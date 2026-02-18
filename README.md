# Setup Instructions for AG-UI

# Prerequisites
- Python 3.10 or later
- Azure OpenAI service endpoint and deployment configured
- Azure CLI installed and authenticated
- User has the Cognitive Services OpenAI Contributor role for the Azure OpenAI resource
- Node.js and npm installed (for Dojo)
- User has AI User RBAC role assigned at the appropriate Foundry Project scope

## AG-UI with Dojo
AG-UI can be used with Dojo to create an interactive experience for building and testing agents. Follow the instructions below to set up AG-UI with Dojo. Dojo requires Node.js and npm to be installed on your machine so that it can serve the AG-UI client application user interface.

## Configure Environment Variables
Create a `.env` file in the root of your project and add the following environment variables:

```env
AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/openai/v1/"
AZURE_OPENAI_DEPLOYMENT_NAME="your-deployment-name"
AGUI_SERVER_URL="http://localhost:8888"
```

## Setup Python Environment

```bash
python -m venv .venv

# On Windows use 
.venv\Scripts\activate

# On Unix or MacOS use
source .venv/bin/activate
```
## Install AG-UI
```bash
pip install agent-framework-ag-ui --pre
```

## Install Asynchronous HTTP Server
```bash
pip install aiohttp
```

## Run the Server
Login to Azure CLI if not already logged in

```bash
python server.py
```

## Run the AG-UI Client
- Open a new Terminal
- Login to Azure CLI if not already logged in
- Activate the Python environment if not already activated

## Open AG-UI in Browser
```bash
python client.py
```

Navigate to `http://localhost:8888` in your web browser to access the AG-UI client interface.

# Troubleshooting

## SDK Version Mismatch
SDK version mismatches can cause issues. Verify that the correct versions of `agent-framework` and `agent-framework-ag-ui` are installed in your Python environment. You can check the installed versions with the following commands:

```bash
.\.venv\Scripts\python.exe -c "from agent_framework import Agent; import inspect; print(inspect.signature(Agent.__init__))"
```

```bash
.\.venv\Scripts\python.exe -c "from agent_framework import Agent; from agent_framework_ag_ui import AGUIChatClient; c=AGUIChatClient(endpoint='http://127.0.0.1:8888/'); a=Agent(client=c,name='ClientAgent',instructions='You are a helpful assistant.'); print(type(a).__name__)"
```

## REST API call
You can use the .http file to test the REST API calls to the AG-UI server. Make sure to update the URL and payload as needed. You can also use tools like Postman or curl to test the API endpoints.

# How To Run Mini DoJo interface with AG-UI server
- Start your agent server from repo root: python .\server.py
- In another terminal: cd mini-dojo then npm start
- Open http://127.0.0.1:3000
- Keep endpoint as http://127.0.0.1:8888/, enter prompt, click Send

# Reference Material
[AG-UI Overview](https://docs.ag-ui.com/introduction)
[AG-UI GitHub Repository](https://github.com/ag-ui-protocol/ag-ui)
[Getting Started with AG-UI](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/getting-started?pivots=programming-language-python)
[Agent Framework Hello Agent Sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/01-get-started/01_hello_agent.py)
[Testing with AG-UI Dojo](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/testing-with-dojo?pivots=programming-language-python)

