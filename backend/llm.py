from langchain_community.chat_models import ChatOpenAI

from backend.config import (
    OPENROUTER_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)


def load_llm():

    return ChatOpenAI(
        model=MODEL_NAME,
        openai_api_key=OPENROUTER_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=TEMPERATURE,
    )