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
        if section not in self.config:
            raise ValueError(f"Section {section} not found in config file")
        return dict(self.config[section])

    def get(self, section, key):
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise ValueError(f"Error reading config: {e}")