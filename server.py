# server.py

# Import necessary libraries and modules
import os
import asyncio

from openai import OpenAI
from agent_framework import Agent
from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework_ag_ui import add_agent_framework_fastapi_endpoint
from azure.identity import AzureCliCredential, DefaultAzureCredential, get_bearer_token_provider

# Import FastAPI for creating the server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Make sure to set the required environment variables in a .env file or your environment:
# Load environment variables from .env file if it exists
from dotenv import load_dotenv
load_dotenv()

# Read required configuration and raise errors if not set
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
project_endpoint = os.environ.get("AZURE_AIPROJECT_ENDPOINT")

if not endpoint:
    raise ValueError("AZURE_OPENAI_ENDPOINT is not set.")

if not deployment_name:
    raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME is not set.")

normalized_endpoint = endpoint.rstrip("/")
if normalized_endpoint.endswith("/openai/v1"):
    normalized_endpoint = normalized_endpoint[: -len("/openai/v1")]

openai_base_url = f"{normalized_endpoint}/openai/v1/"

print(f"Using Azure OpenAI Endpoint: {normalized_endpoint}")
print(f"Using Azure OpenAI Deployment Name: {deployment_name}")

# Use OpenAI SDK to generate a response
print("Using Azure OpenAI SDK to generate a response")

# Ask the user a prompt to test the Azure OpenAI client
prompt = input("Enter a prompt to test Azure OpenAI client (or press Enter to use default): ")

if not prompt.strip():
    prompt = "What is the capital of France?"

# Set up token provider for Azure OpenAI client
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default")

# Create Azure OpenAI client and test a response
client = OpenAI(
    base_url=openai_base_url,
    api_key=token_provider
)

response = client.responses.create(
    model=deployment_name,
    input=prompt,
)

print(f"answer: {response.output[0]}")

# Ask the user and get approval to continue
proceed = input("Do you wish to continue loading the server? (y/n): ")

if proceed.lower() != "y":
    print("Thanks! Catch you later.")
    exit(1)

print("Great! Now let's test a prompt using the Agent Framework AzureOpenAIChatClient and then start the server...")

# Ask the user to enter a prompt to test the agent, or use a default one
agent_prompt = input("Enter a prompt to test the agent (or press Enter to use default): ")

if not agent_prompt.strip():
    agent_prompt = "What is Microsoft Agent Framework?"

# Create Azure OpenAI chat client using Agent Framework's built-in AzureOpenAIChatClient
credential = AzureCliCredential()

client = AzureOpenAIChatClient(
    credential=credential,
    endpoint=normalized_endpoint,
    deployment_name=deployment_name,
)

# Did we create the client successfully? Is the client instantiated or not?
if client is not None:
    print("Successfully created Azure OpenAI Chat Client using Agent Framework's AzureOpenAIChatClient!")

# Create an agent with the Azure OpenAI chat client and some basic instructions
agent = Agent(
    name="foundry-agui-server-agent",
    instructions="You are a friendly digital assistant. Keep your answers brief and professional. Only answer from what you know and have studied. If you don't know the answer, say you don't know. Always be concise and to the point.",
    client=client,
)

# Non-streaming: run a test query to verify the agent is working
result = agent.run(agent_prompt)
print(f"Agent: {result}")

# Create FastAPI app
app = FastAPI(title="Foundry Agent Framework AG-UI Server")

# Add CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the AG-UI endpoint
add_agent_framework_fastapi_endpoint(app, agent, "/")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8888)