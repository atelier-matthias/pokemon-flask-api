from os import path


class BaseConfig:
    BASE_PATH = path.dirname(path.dirname(path.abspath(__file__)))
    DEBUG = True
    TESTING = True
    MONGO_URI = 'mongodb://localhost:27017/pokemon-develop'
    SERVER_NAME = '0.0.0.0:8989'
    REDIS_URL = "redis://redis:6379"
    POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


class ProductionConfig(BaseConfig):
    MONGO_URI = 'mongodb://localhost:27017/pokemon'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    MONGO_URI = 'mongodb://localhost:27017/pokemon-develop'
    REDIS_URL = "redis://localhost:6379"
    DEBUG = True
    TESTING = True


class TestingConfig(BaseConfig):
    MONGO_URI = 'mongodb://localhost:27017/pokemon-testing'
    TESTING = True


ENV_MAP = {
    "testing": TestingConfig,
    "develop": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}