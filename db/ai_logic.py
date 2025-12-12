import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv() # Load environment variables from .env file

# Initialize Azure ChatCompletionsClient
client = ChatCompletionsClient(
    endpoint="https://models.github.ai/inference",
    credential=AzureKeyCredential(os.environ["ApiKey"]),
    api_version="2024-12-01-preview",
)

# Initialize message history with system instructions
messages=[
    SystemMessage("You are a helpful assistant that is called Skrotnissen."),
    SystemMessage("You answer in a friendly, concise manner and as short as possible without losing any detail or helpfullness."),
    SystemMessage("You help users with finding products in our store."),
    SystemMessage("Do not use asteriks (*) in your answers. Change them out with <br><b> and </b><br> tags for bolding text."),
    SystemMessage("If you're making any kind of list, make sure to use <br> tags to seperate the items in the list."),
]

def get_ai_response(userInput: str, database: dict) -> str:
    global messages

    messages.append(SystemMessage(f"Here is the product database: {database}")) # Add the product database to the system message for context
    messages.append(UserMessage(userInput)) # Add user input to message history

    # Get AI response from the model
    response = client.complete(
        messages=messages,
        model="gpt-4o-mini"
    )

    ai_response = response.choices[0].message.content # Extract AI's reply

    messages.append(AssistantMessage(ai_response)) # Add AI's response to message history

    return ai_response # Return the AI's response