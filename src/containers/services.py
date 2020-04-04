from flask_redis import FlaskRedis

from containers import (
    SubContainer,
    BaseContainer,
    cached_property,
)
from pokemons.services import PokemonApiService


class ServiceContainer(SubContainer):
    def __init__(self, parent: BaseContainer) -> None:
        super().__init__(parent)

    @cached_property
    def pokemon_service(self) -> PokemonApiService:
        return PokemonApiService(self._parent.app.config['POKEAPI_BASE_URL'])

    @cached_property
    def redis_client(self) -> FlaskRedis:
        return FlaskRedis(self._parent.app)
