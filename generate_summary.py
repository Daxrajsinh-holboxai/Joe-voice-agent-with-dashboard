from openai import OpenAI
import os

# using openai to generate summary
async def generate_summary(conversation: list) -> str:
    """
    Summarizes the entire conversation between USER and ASSISTANT.
    Takes in the conversation list, then generates a summary.
    """
    if not conversation or len(conversation) == 0:
        return "No conversation to summarize."

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
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
    )

    try:
        # Send the conversation to OpenAI for summarization
        response = client.responses.create(
            model="gpt-4o-mini",  # You can use a different model here
            temperature=0.2,
            instructions = "Summarize the following conversation between user and assistant. Make it concise and clear.",
            input= f"Conversation:\n{formatted_conversation}\n\nProvide a summary of the conversation."
            # messages=[
            #     {"role": "system", "content": "Summarize the following conversation between user and assistant. Make it concise and clear."},
            #     {"role": "user", "content": f"Conversation:\n{formatted_conversation}\n\nProvide a summary of the conversation."}
            # ],
        )

        summary = response.output_text
        return summary

    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Summary unavailable due to an error."
