from os import path


class BaseConfig:
    BASE_PATH = path.dirname(path.dirname(path.abspath(__file__)))
    DEBUG = True
    TESTING = True
    DB_NAME = 'pokemon'
    MONGO_URI = f'mongodb://localhost:27017/{DB_NAME}'
    SERVER_NAME = '0.0.0.0:8989'
    REDIS_URL = "redis://redis:6379"
    POKEAPI_BASE_URL = "https://pokeapi.co/api/v2"


class ProductionConfig(BaseConfig):
    DB_NAME = 'pokemon'
    MONGO_URI = f'mongodb://localhost:27017/{DB_NAME}'
    DEBUG = False
    TESTING = False


class DevelopmentConfig(BaseConfig):
    DB_NAME = 'pokemon-develop'
    MONGO_URI = f'mongodb://localhost:27017/{DB_NAME}'
    REDIS_URL = "redis://localhost:6379"
    DEBUG = True
    TESTING = False


class DockerConfig(BaseConfig):
    DB_NAME = 'pokemon'
    MONGO_URI = f'mongodb://mongo:27017/{DB_NAME}'
    REDIS_URL = "redis://redis:6379"
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    DB_NAME = 'pokemon-testing'
    MONGO_URI = f'mongodb://localhost:27017/{DB_NAME}'
    TESTING = False


class TestsConfig(BaseConfig):
    DB_NAME = 'pokemon-tests'
    MONGO_URI = f'mongodb://mongo:27017/{DB_NAME}'
    REDIS_URL = "redis://redis:6379"
    TESTING = True


ENV_MAP = {
    "testing": TestingConfig,
    "develop": DevelopmentConfig,
    "docker": DockerConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}