from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import settings

def get_llm(temperature: float = 0.0) -> BaseChatModel:
    """Returns a configured LLM instance based on the provider in settings."""
    provider = settings.LLM_PROVIDER.lower()
    
    if provider == "anthropic":
        return ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            anthropic_api_key=settings.ANTHROPIC_API_KEY,
            temperature=temperature
        )
    elif provider == "openai":
        return ChatOpenAI(
            model=settings.OPENAI_MODEL,
            api_key=settings.OPENAI_API_KEY,
            temperature=temperature
        )
    elif provider == "google":
        return ChatGoogleGenerativeAI(
            model=settings.GOOGLE_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=temperature
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

