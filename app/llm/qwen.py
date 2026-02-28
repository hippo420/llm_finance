from langchain_community.chat_models import ChatOllama

def get_qwen_llm():
    """
    Qwen LLM 설정
    - Ollama 로컬 실행 기준
    - 나중에 OpenAI / vLLM / TGI로 교체 가능
    """

    return ChatOllama(
        model="qwen:7b",
        temperature=0,
        timeout=60
    )