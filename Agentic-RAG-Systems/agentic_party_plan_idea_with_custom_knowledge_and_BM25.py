from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from smolagents import Tool
from langchain_community.retrievers import BM25Retriever
from smolagents import CodeAgent, InferenceClientModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize the model
model = InferenceClientModel(
    token = HF_TOKEN
)

agent = CodeAgent(
    model=model,
    tools=[],
)

# Example usage
response = agent.run(
    "Search for luxury superhero-themed party ideas, including decorations, entertainment, and catering."
)
print(response)