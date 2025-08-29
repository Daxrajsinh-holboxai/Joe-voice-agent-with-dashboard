from openai import OpenAI
import os

# using openai to generate summary
async def generate_summary(conversation: list) -> dict:
    """
    Summarizes the entire conversation and retrieves customer name (via LLM).
    Returns a JSON-like dictionary containing 'cust_name' and 'summary'.
    """
    if not conversation or len(conversation) == 0:
        return {"cust_name": "Unknown", "summary": "No conversation to summarize."}

    # Format the conversation into a string format, keeping user and assistant messages clearly separated
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
        # Send the conversation to OpenAI for summarization
        response = client.responses.create(
            model="gpt-4o-mini",  # Use the model you prefer
            temperature=0.2,
            instructions=(
                "Summarize the following conversation and identify the customer's name, if mentioned. "
                "The response should include both the name of the customer (if available) and a concise summary of the conversation, "
                "highlighting the customer's details, symptoms, and the assistant's suggestions. "
                "Your response should be in strictly JSON format, like this: "
                '{ "cust_name" : <Customer name that it has provided throughout the conversation>, "summary": <Summary of the whole conversation> }'
            ),
            input=f"Conversation:\n{formatted_conversation}\n\nProvide a summary of the conversation with the customer's name."
        )

        result = response.output_text.strip()

        # Attempt to extract the customer's name and summary from the response
        if "Name:" in result:
            parts = result.split("Name:")
            cust_name = parts[1].split("\n")[0].strip()  # Extract the name after 'Name:'
            summary = parts[0].strip()  # The remaining part is the summary
        else:
            cust_name = "Unknown"
            summary = result

        # Return the response in the desired JSON format
        return {"cust_name": cust_name, "summary": summary}

    except Exception as e:
        print(f"Error generating summary: {e}")
        return {"cust_name": "Unknown", "summary": "Summary unavailable due to an error."}