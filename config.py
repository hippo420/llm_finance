import configparser
import os

class Config:
    def __init__(self, config_file="config.ini"):
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        self.config.read(self.config_file)

    def get_db_config(self):
        section = "PostgreSQL"
        if section not in self.config:
            raise ValueError(f"Section {section} not found in config file")
        return dict(self.config[section])

    def get_es_config(self):
        section = "ElasticSearch"
        if section not in self.config:
            raise ValueError(f"Section {section} not found in config file")
        return dict(self.config[section])

    def get_llm_config(self):
        section = "LLM"
        defaults = {
            "model_name": "qwen2.5:7b",
            "temperature": "0.1",
            "base_url": "http://localhost:11434"
        }
        if section not in self.config:
            return defaults

        # config.ini 파일의 값으로 기본값을 덮어씁니다.
        conf = defaults.copy()
        conf.update(dict(self.config[section]))
        return conf

    def get_chroma_config(self):
        section = "Chroma"
        # Default to localhost:8000 if not in config, per requirements
        if section not in self.config:
            return {"host": "localhost", "port": "8000", "collection_name": "schema_store"}
        return dict(self.config[section])

    def get_server_config(self):
        section = "Server"
        defaults = {"host": "0.0.0.0", "port": "31111"}
        if section not in self.config:
            return defaults
        
        return dict(self.config[section])

    def get(self, section, key):
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise ValueError(f"Error reading config: {e}")