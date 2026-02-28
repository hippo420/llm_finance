from elasticsearch import Elasticsearch
from app.config import Config

def create_es_client():
    config = Config()
    es_config = config.get_es_config()

    host = es_config.get('host', 'localhost')
    port = es_config.get('port', '9200')
    scheme = es_config.get('scheme', 'http')
    user = es_config.get('user')
    password = es_config.get('password')

    url = f"{scheme}://{host}:{port}"

    if user and password:
        es_client = Elasticsearch(url, basic_auth=(user, password))
    else:
        es_client = Elasticsearch(url)

    return es_client

if __name__ == '__main__':
    es_client = create_es_client()
    
    if es_client.ping():
        print("Connected to Elasticsearch")