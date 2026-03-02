from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from app.config import Config

def create_db_engine():
    config = Config()
    db_config = config.get_db_config()
    
    url_object = URL.create(
        "postgresql",
        username=db_config['user'],
        password=db_config['password'],
        host=db_config['host'],
        port=int(db_config['port']),
        database=db_config['database']
    )
    engine = create_engine(url_object)
    return engine

if __name__ == '__main__':
    engine = create_db_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.scalar())