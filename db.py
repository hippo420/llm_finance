from sqlalchemy import create_engine, text
from app.config import Config

def create_db_engine():
    config = Config()
    db_config = config.get_db_config()
    
    DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
    engine = create_engine(DATABASE_URL)
    return engine

if __name__ == '__main__':
    engine = create_db_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.scalar())