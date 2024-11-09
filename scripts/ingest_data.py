import argparse
import json
import os
import time

from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from tqdm import tqdm

from loaders.text_loaders import TextLoaderWithMetadata

parser = argparse.ArgumentParser(description="Ingest data into Pinecone")
parser.add_argument(
    "-c", "--config", type=str, help="Path to the config file", required=True
)
parser.add_argument(
    "-e",
    "--env",
    default=".env",
    type=str,
    help="[Optional] Path to the environment file",
)
args = parser.parse_args()

load_dotenv(args.env)
with open(args.config, "r") as f:
    config = json.load(f)

# prepare modules for document extraction
loader = TextLoaderWithMetadata(config["data_path"])
documents = loader.load(metadata=config["metadata"])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=0
)
docs = text_splitter.split_documents(documents)

embeddings_model = AzureOpenAIEmbeddings(
    azure_deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

print("Documents: ", len(docs))

PC = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
PC_INDEX_NAME = os.environ["PINECONE_INDEX_NAME"]

print("Pinecone Indexes: ", PC.list_indexes())

BATCH_SIZE = 100
progress_bar = tqdm(total=len(docs), desc="Processing batches")
for i in range(0, len(docs), BATCH_SIZE):
    batch = docs[i : i + BATCH_SIZE]
    vectorstore = PineconeVectorStore.from_documents(
        batch, embeddings_model, index_name=PC_INDEX_NAME
    )
    time.sleep(60)
    progress_bar.update(len(batch))
progress_bar.close()

print("Done!")
