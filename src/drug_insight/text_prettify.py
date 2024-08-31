import os
from typing import Optional

from dotenv import load_dotenv
from langchain.chains import create_structured_output_runnable
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders.text import TextLoader
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import AzureChatOpenAI
from langchain_text_splitters.base import TextSplitter
from openai import BadRequestError
from pydantic.v1 import ValidationError

load_dotenv(".env")

openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"]
azure_deployment = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
azure_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]


def prettify_text(doc_dir: str, output_dir: str):
    """
    Processes text data about drugs from .txt file, cleans and structures it using an AI model, and writes the structured output to a new .txt file.

    Args:
    - doc_dir (str): Directory to .txt file containing raw text data about drugs.
    - output_dir (str): Directory .txt file to write the structured output data.

    Returns:
    - None
    - The function writes the structured output directly to a new .txt file.

    This function loads raw text data, structures it according to specified drug details schema, and writes the structured output to a new .txt file.
    """

    # Load and split text into manageable chunks
    text_chunks = TextLoader(doc_dir).load_and_split()

    # Define a data schema for drug information of interest
    class Drug(BaseModel):
        """The schema to record the important information about a drug."""

        name: str = Field(..., description="The drug's name")
        diseases_and_usecases: str = Field(
            ...,
            description="List the diseases and conditions that the drug is used to treat",
        )
        warnings: str = Field(
            ...,
            description="Mention any warnings associated with the use of the drug",
        )
        indications: str = Field(
            ...,
            description="Describe the specific indications for using the drug",
        )
        contraindications: str = Field(
            ...,
            description="List the conditions or factors that would make the use of the drug inadvisable",
        )
        dosages_and_how_it_should_be_taken: str = Field(
            ...,
            description="Provide detailed information on the recommended dosages and how the drug should be administered",
        )
        what_happens_if_i_miss_a_dose: str = Field(
            ..., description="Explain the steps to take if a dose is missed"
        )
        what_happens_if_i_overdose: str = Field(
            ...,
            description="Describe the actions to take and potential consequences of an overdose",
        )
        what_should_i_avoid_while_taking_the_medication: str = Field(
            ...,
            description="List any activities, foods, or other drugs to avoid while taking the medication",
        )
        side_effects: str = Field(
            ...,
            description="Provide a list of potential side effects of the drug",
        )
        drugs_that_cause_interactions: str = Field(
            ...,
            description="Mention other drugs that may interact with this medication and the nature of those interactions",
        )

    # Initialize the GPT model for structured output generation

    llm = AzureChatOpenAI(
        openai_api_version, azure_deployment, api_key, azure_endpoint
    )

    # Define the prompt template for the model
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are provided with raw text data containing information about various drugs. Your task is to clean and structure this data to \
          ensure that it contains the specified details for each drug. Ensure the information is accurate, concise, and clearly organized under each category. \
          Remove any redundant or irrelevant data, and verify the completeness of the extracted details for each drug.",
            ),
            ("human", "{input}"),
        ]
    )

    # Create a runnable instance for structured output generation
    structured_llm = create_structured_output_runnable(
        Drug,
        llm,
        mode="openai-tools",
        enforce_function_usage=True,
        return_single=True,
    )

    # Process each chunk of text and write structured output to file
    for chunk in text_chunks:
        try:
            info = structured_llm.invoke(str(chunk))
            with open(output_dir, "a") as f:
                f.write("\n" + "\n" + str(info))

        except (BadRequestError, ValidationError) as e:
            continue
