from openai import OpenAI
import os
import json
import re

async def generate_summary(conversation: list) -> dict:
    """
    Summarizes the entire conversation and retrieves customer name (via LLM).
    Returns a JSON-like dictionary containing 'cust_name' and 'summary'.
    """
    if not conversation or len(conversation) == 0:
        return {"cust_name": "Unknown", "summary": "No conversation to summarize."}

    # Format the conversation into a string format
    formatted_conversation = ""
    
    for entry in conversation:
        user_message = entry.get("user_message", "").strip()
        assistant_message = entry.get("assistant_message", "").strip()
        
        if user_message:
            formatted_conversation += f"USER: {user_message}\n"
        if assistant_message:
            formatted_conversation += f"ASSISTANT: {assistant_message}\n"

    # Initialize OpenAI API client
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    try:
        # Use the chat.completions endpoint instead of responses.create
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that summarizes conversations. "
                        "Your response must be valid JSON only with this exact structure: "
                        '{ "cust_name": "customer name", "summary": "conversation summary" }'
                    )
                },
                {
                    "role": "user",
                    "content": f"Please summarize this conversation and extract the customer's name:\n\n{formatted_conversation}"
                }
            ],
            response_format={"type": "json_object"}
        )

        # Extract the JSON response
        result = response.choices[0].message.content.strip()
        
        # Try to parse as JSON
        try:
            summary_data = json.loads(result)
            return summary_data
        except json.JSONDecodeError:
            # If it's not valid JSON, try to extract name and summary manually
            cust_name_match = re.search(r'"cust_name":\s*"([^"]*)"', result)
            summary_match = re.search(r'"summary":\s*"([^"]*)"', result)
            
            if cust_name_match and summary_match:
                return {
                    "cust_name": cust_name_match.group(1),
                    "summary": summary_match.group(1)
                }
            else:
                # Fallback if we can't extract the fields
                return {"cust_name": "Unknown", "summary": result}
            
    except Exception as e:
        print(f"Error generating summary: {e}")
        return {"cust_name": "Unknown", "summary": f"Summary unavailable due to an error: {str(e)}"}