from containers import (
    SubContainer,
    BaseContainer,
    cached_property,
)

from encounters.commands import (
    CreateEncounterCommand,
    SearchEncounterCommand,
)
from pokemons.commands import (
    SearchPokemonsCommand,
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
    def search_pokemons(self) -> SearchPokemonsCommand:
        return SearchPokemonsCommand(self._repositories.pokemons)

    @cached_property
    def create_pokemon(self) -> CreatePokemonCommand:
        return CreatePokemonCommand(self._repositories.pokemons,
                                    self._parent.services.pokemon_service,
                                    self._parent.services.redis_client)

    @cached_property
    def initialize_redis_pokemon_data(self) -> InitializePokemonRedisCommand:
        return InitializePokemonRedisCommand(self._parent.services.pokemon_service,
                                             self._parent.services.redis_client)

    @cached_property
    def create_encounter(self) -> CreateEncounterCommand:
        return CreateEncounterCommand(self._repositories.encounters,
                                      self._repositories.pokemons)

    @cached_property
    def search_encounters(self) -> SearchEncounterCommand:
        return SearchEncounterCommand(self._repositories.encounters)
