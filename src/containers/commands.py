from containers import (
    SubContainer,
    BaseContainer,
    cached_property,
)

# noinspection PyAttributeOutsideInit
from pokemons.commands import (
    FetchPokemonsCommand,
    CreatePokemonCommand,
    InitializePokemonRedisCommand,
)


class CommandContainer(SubContainer):
    def __init__(self, parent: BaseContainer):
        for item in self.__slots__:
            setattr(self, item, None)
        super().__init__(parent)
        self._repositories = parent.repositories
        self.config = parent.app.config

    @cached_property
    def fetch_pokemons(self) -> FetchPokemonsCommand:
        return FetchPokemonsCommand(self._repositories.pokemons)

    @cached_property
    def create_pokemon(self) -> CreatePokemonCommand:
        return CreatePokemonCommand(self._repositories.pokemons,
                                    self._parent.services.pokemon_service,
                                    self._parent.services.redis_client)

    @cached_property
    def initialize_redis_pokemon_data(self) -> InitializePokemonRedisCommand:
        return InitializePokemonRedisCommand(self._parent.services.pokemon_service,
                                             self._parent.services.redis_client)
