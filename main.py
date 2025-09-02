import asyncio
import base64
import json
import sys
import websockets
import ssl
import os
from dotenv import load_dotenv
from agent_function import FUNCTION_MAP
from generate_summary import generate_summary
load_dotenv()

# Store connected frontend clients
frontend_clients = set()
full_transcript = {}
all_conversation = {}

async def broadcast_to_frontend(data):
    if not frontend_clients:
        return
    message = json.dumps(data)
    disconnected = []
    for ws in list(frontend_clients):
        try:
            await ws.send(message)
        except Exception:
            disconnected.append(ws)
    for ws in disconnected:
        frontend_clients.remove(ws)


def sts_connect():
    api_key = os.getenv('DEEPGRAM_API_KEY')
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is not set")

    sts_ws = websockets.connect(
        "wss://agent.deepgram.com/v1/agent/converse",
        subprotocols=["token", api_key]
    )
    return sts_ws

def load_config():
    with open("config.json", "r") as f:
        return json.load(f)

def execute_function_call(func_name, arguments):
    if func_name in FUNCTION_MAP:
        result = FUNCTION_MAP[func_name](**arguments)
        print(f"Function call result: {result}")
        return result
    else:
        result = {"error": f"Unknown function: {func_name}"}
        print(result)
        return result

def create_function_call_response(func_id, func_name, result):
    return {
        "type": "FunctionCallResponse",
        "id": func_id,
        "name": func_name,
        "content": json.dumps(result)
    }

async def handle_function_call_request(decoded, sts_ws):
    try:
        for function_call in decoded["functions"]:
            func_name = function_call["name"]
            func_id = function_call["id"]
            arguments = json.loads(function_call["arguments"])
            print(f"Function call: {func_name} (ID: {func_id}), arguments: {arguments}")

            result = execute_function_call(func_name, arguments)

            function_result = create_function_call_response(func_id, func_name, result)
            await sts_ws.send(json.dumps(function_result))
            print(f"Sent function result: {function_result}")

    except Exception as e:
        print(f"Error calling function: {e}")
        error_result = create_function_call_response(
            func_id if "func_id" in locals() else "unknown",
            func_name if "func_name" in locals() else "unknown",
            {"error": f"Function call failed with: {str(e)}"}
        )
        await sts_ws.send(json.dumps(error_result))

async def handle_barge_in(decoded, twilio_ws, streamsid):
    if decoded["type"] == "UserStartedSpeaking":
        clear_message = {
            "event": "clear",
            "streamSid": streamsid
        }
        await twilio_ws.send(json.dumps(clear_message))

async def handle_full_transcript(decoded, twilio_ws, streamsid, callsid):
    if decoded['type'] == 'ConversationText':
        role = decoded.get('role')
        content = decoded.get('content', '').strip()
        global full_transcript
        global all_conversation
        if role == 'user' and content:
            print(f"\033[92mUser:\033[0m {content}")  # Green
            # Update the full transcription
            
            if callsid not in full_transcript:
                full_transcript[callsid] = ""
            
            full_transcript[callsid] += content
            # print(full_transcript)

            await broadcast_to_frontend({
                "type": "transcription",
                "data": {
                    "call_sid": callsid,
                    "message": full_transcript[callsid]
                }
            })

        elif role == 'assistant' and content:
            print(f"\033[94mAssistant:\033[0m {content}")  # Blue
            if callsid not in all_conversation:
                all_conversation[callsid] = []
            
            all_conversation[callsid].append({
                "user_message": full_transcript.get(callsid, ""),
                "assistant_message": content
            })
            await broadcast_to_frontend({
                "type": "ai_response",
                "data": {
                    "call_sid": callsid,
                    "message": content
                }
            })

async def handle_text_message(decoded, twilio_ws, sts_ws, streamsid, callsid):
    await handle_barge_in(decoded, twilio_ws, streamsid)
    await handle_full_transcript(decoded, twilio_ws, streamsid, callsid)

    if decoded["type"] == "FunctionCallRequest":
        await handle_function_call_request(decoded, sts_ws)

async def twilio_handler(twilio_ws):
    audio_queue = asyncio.Queue()
    streamsid_queue = asyncio.Queue()

    async with sts_connect() as sts_ws:
        config_message = load_config()

        await sts_ws.send(json.dumps(config_message))
        async def sts_sender(sts_ws):
            while True:
                chunk = await audio_queue.get()
                if isinstance(chunk, bytes):  # Ensure we're sending bytes
                    await sts_ws.send(chunk)
                else:
                    print(f"Unexpected data type in queue: {type(chunk)}")
                    break

        async def sts_receiver(sts_ws):
            start_info = await streamsid_queue.get()  # First get the start_info
            streamsid = start_info["streamSid"]
            callsid = start_info["callSid"]
            caller = start_info.get("from", "Customer")
            callee = start_info.get("to", "AI Agent")
            
            # Notify frontend about new call with all details
            await broadcast_to_frontend({
                "type": "incoming_call",
                "data": {
                    "CallSid": callsid,
                    "From": caller,  # Include caller number
                    "To": callee,   # Include callee number
                    "status": "in_progress",
                    "messages": []
                }
            })

            async for message in sts_ws:
                if isinstance(message, str):
                    decoded = json.loads(message)
                    await handle_text_message(decoded, twilio_ws, sts_ws, streamsid, callsid)
                    continue
                raw_mulaw = message

                media_message = {
                    "event": "media",
                    "streamSid": streamsid,
                    "media": {"payload": base64.b64encode(raw_mulaw).decode("ascii")},
                }

                await twilio_ws.send(json.dumps(media_message))
                global full_transcript
                full_transcript[callsid] = ""

        async def twilio_receiver(twilio_ws):
            BUFFER_SIZE = 20 * 160

            inbuffer = bytearray(b"")
            async for message in twilio_ws:
                try:
                    data = json.loads(message)
                    event_type = data["event"]

                    if event_type == "start":
                        # Extract custom parameters from the start event
                        custom_params = data["start"].get("customParameters", {})
                        from_number = custom_params.get("from", "Unknown")
                        to_number = custom_params.get("to", "Unknown")

                        print("from_number:", from_number)
                        print("to_number:", to_number)

                        streamsid_queue.put_nowait({
                            "streamSid": data["start"]["streamSid"],
                            "callSid": data["start"]["callSid"],
                            "from": from_number,  # Now includes the actual caller number
                            "to": to_number      # Now includes the called number
                        })

                    elif event_type == "media" and "payload" in data["media"]:
                        # Process inbound audio only
                        if data["media"].get("track") == "inbound":
                            chunk = base64.b64decode(data["media"]["payload"])
                            inbuffer.extend(chunk)
                            
                            # Process complete chunks
                            while len(inbuffer) >= BUFFER_SIZE:
                                await audio_queue.put(bytes(inbuffer[:BUFFER_SIZE]))
                                del inbuffer[:BUFFER_SIZE]

                    elif event_type == "stop":
                        callsid = data["stop"]["callSid"]
                        global all_conversation
                        
                        try:
                            # Get the summary and customer name from the async function
                            summary = await generate_summary(all_conversation.get(callsid, []))
                            
                            # Extract customer name and conversation summary
                            cust_name = summary.get("cust_name", "Unknown")
                            conversation_summary = summary.get("summary", "Summary unavailable")
                            
                            # Print for debugging (optional)
                            print(f"Customer Name: {cust_name}")
                            print(f"Conversation Summary: {conversation_summary}")
                            
                        except Exception as e:
                            # Handle any errors that occurred during summary generation
                            print(f"Error during summary generation: {e}")
                            cust_name = "Unknown"
                            conversation_summary = "Summary unavailable"

                        # Sending the summary and status to the frontend
                        await broadcast_to_frontend({
                            "type": "call_summary",
                            "data": {
                                "CallSid": callsid,
                                "summary": conversation_summary,
                                "name": cust_name
                            }
                        })

                        # Broadcast the call completion status
                        await broadcast_to_frontend({
                            "type": "call_status",
                            "data": {
                                "CallSid": callsid,
                                "CallStatus": "completed"
                            }
                        })

                        break

                except Exception as e:
                    print(f"Error in twilio_receiver: {e}")
                    break
        await asyncio.wait(
            [
                asyncio.ensure_future(sts_sender(sts_ws)),
                asyncio.ensure_future(sts_receiver(sts_ws)),
                asyncio.ensure_future(twilio_receiver(twilio_ws)),
            ]
        )
        await twilio_ws.close()


# WebSocket router
async def router(websocket, path):
    if path == "/twilio":
        print("\033[93mIncoming call on /twilio — starting Twilio handler\033[0m")
        await twilio_handler(websocket)
    elif path == "/frontend-updates":
        print("\033[96mFrontend client connected\033[0m")
        frontend_clients.add(websocket)
        try:
            async for _ in websocket:
                pass
        finally:
            frontend_clients.remove(websocket)

# Entry point
def main():
    server = websockets.serve(router, "0.0.0.0", 5001)
    print(f"Server starting on {os.getenv('BACKEND_URL')}")
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    sys.exit(main() or 0)