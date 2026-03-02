from langchain_community.chat_models import ChatOllama
from app.config import Config

def load_llm():
    config = Config()
    llm_config = config.get_llm_config()

    model_name = llm_config["model_name"]
    temperature = float(llm_config["temperature"])
    base_url = llm_config["base_url"]

    print(f"Loading LLM: {model_name} at {base_url} with temperature {temperature}")

    llm = ChatOllama(
        model=model_name,
        temperature=temperature,
        base_url=base_url
    )
    return llm