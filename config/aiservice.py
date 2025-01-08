from config.ai_config_schema import LLM, EMBEDDING
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from agent import PhiAgent
from typing import Optional, List
from loguru import logger



def get_llm(model_name: str):
    model_config = {
        "gpt-4o-mini": ChatOpenAI,
        "gpt-4-turbo": ChatOpenAI,
        "gpt-4": ChatOpenAI,
        "azure-gpt-4o-mini": AzureChatOpenAI,
        "azure-gpt-4-turbo": AzureChatOpenAI,
        "azure-gpt-4": AzureChatOpenAI,
        "gemini-pro": ChatGoogleGenerativeAI,
        "gemini-flash": ChatGoogleGenerativeAI,
        "gemini-2.0-flash": ChatGoogleGenerativeAI,
        "claude-pro": ChatAnthropic,
        "claude-fast": ChatAnthropic,
        "claude-medium": ChatAnthropic,
    }
    logger.info(f"Model name: {model_name}")
    llm_class = model_config.get(model_name)
    if llm_class:
        kwargs = {
            "model": LLM[model_name]["model"],
            "temperature": 0,
            "max_tokens": LLM[model_name]["max_tokens"],
        }
        if llm_class == ChatGoogleGenerativeAI:
            kwargs["convert_system_message_to_human"] = True

        if llm_class == ChatOpenAI:
            kwargs["stream_usage"] = True

        llm = llm_class(**kwargs)
        return llm
    raise ValueError(f"Unsupported model name: {model_name}")


def run_agent(
    model_name: str,
    system_prompt: str,
    tools: Optional[List] = None,

):
    llm = get_llm(model_name)

    agent_instance = PhiAgent(llm=llm, tools=tools, system_prompt=system_prompt)
    config = {"configurable": {"thread_id": "1"}}
    return (
        agent_instance.compile(),
        config,
        agent_instance.memory,
    )