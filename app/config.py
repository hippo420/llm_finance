import configparser
import os

class Config:
    """
    Configuration class to load settings from config.ini
    """
    # Determine the absolute path to the project root (parent of app/)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CONFIG_PATH = os.path.join(BASE_DIR, 'config.ini')

    _config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        _config.read(CONFIG_PATH)

    # PostgreSQL
    POSTGRES_HOST = _config.get('PostgreSQL', 'host', fallback='localhost')
    POSTGRES_PORT = _config.getint('PostgreSQL', 'port', fallback=5432)
    POSTGRES_DB = _config.get('PostgreSQL', 'database', fallback='finadm')
    POSTGRES_USER = _config.get('PostgreSQL', 'user', fallback='finadm')
    POSTGRES_PASSWORD = _config.get('PostgreSQL', 'password', fallback='1234')

    # ElasticSearch
    ES_HOST = _config.get('ElasticSearch', 'host', fallback='localhost')
    ES_PORT = _config.getint('ElasticSearch', 'port', fallback=9200)
    ES_SCHEME = _config.get('ElasticSearch', 'scheme', fallback='http')
    ES_USER = _config.get('ElasticSearch', 'user', fallback='')
    ES_PASSWORD = _config.get('ElasticSearch', 'password', fallback='')

    # LLM
    LLM_MODEL_NAME = _config.get('LLM', 'model_name', fallback='qwen2.5:7b')
    LLM_TEMPERATURE = _config.getfloat('LLM', 'temperature', fallback=0.1)
    LLM_BASE_URL = _config.get('LLM', 'base_url', fallback='http://localhost:11434')

    # ChromaDB
    CHROMA_HOST = _config.get('ChromaDB', 'host', fallback='localhost')
    CHROMA_PORT = _config.getint('ChromaDB', 'port', fallback=8000)
    CHROMA_COLLECTION_NAME = _config.get('ChromaDB', 'collection_name', fallback='finance')

    @classmethod
    def get_chroma_config(cls):
        return {
            'host': cls.CHROMA_HOST,
            'port': cls.CHROMA_PORT,
            'collection_name': cls.CHROMA_COLLECTION_NAME
        }

    @classmethod
    def get_llm_config(cls):
        return {
            'model_name': cls.LLM_MODEL_NAME,
            'temperature': cls.LLM_TEMPERATURE,
            'base_url': cls.LLM_BASE_URL
        }

    @classmethod
    def get_db_config(cls):
        """
        Get the database configuration.
        """
        return {
            'host': cls.POSTGRES_HOST,
            'port': cls.POSTGRES_PORT,
            'database': cls.POSTGRES_DB,
            'user': cls.POSTGRES_USER,
            'password': cls.POSTGRES_PASSWORD
        }