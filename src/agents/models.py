from typing import Any, Dict

# from langchain.chat_models import ChatOpenAI
from langchain_openai import AzureChatOpenAI, ChatOpenAI

MODEL_FACTORY = {
    "chat_openai": ChatOpenAI,
    "azure_chat_openai": AzureChatOpenAI,
}


def get_model(model_name=str, model_params=Dict) -> Any:
    """Function to get a model instance.

    Args:
        model_name (str, optional): name of model. Defaults to str.
        model_params (Dict, optional): model parameters. Defaults to Dict.

    Returns:
        Any: Returns a model instance.
    """
    return MODEL_FACTORY[model_name](**model_params)
