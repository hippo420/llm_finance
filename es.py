from elasticsearch import Elasticsearch
from app.config import Config

def create_es_client():
    config = Config()
    es_config = config.get_es_config()

    es_client = Elasticsearch(
        cloud_id=es_config.get('cloud_id'),
        api_key=es_config.get('api_key')
    )
    return es_client

if __name__ == '__main__':
    es_client = create_es_client()
    
    if es_client.ping():
        print("Connected to Elasticsearch")