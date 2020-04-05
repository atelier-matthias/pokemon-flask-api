from typing import (
    List,
    Tuple,
    Optional,
)

from flask_redis import FlaskRedis

from commons.commands import (
    Sort,
    Pagination,
)
from pokemons.mappers import ExternalPokeApiValidationException
from pokemons.model import Pokemon
from pokemons.repository import PokemonsRepository
from pokemons.services import (
    PokemonApiService,
    PokemonApiException,
)


class PokemonNotFoundException(Exception):
    __slots__ = ()


class PokemonExternalServiceException(Exception):
    __slots__ = ('message',)

    def __init__(self, message: str):
        self.message = message


class PokemonsCommand:
    __slots__ = ('pokemons_repository',)

    def __init__(self, pokemons_repository: PokemonsRepository):
        self.pokemons_repository = pokemons_repository


class InitializePokemonRedisCommand:
    __slots__ = ('pokemon_service', 'redis_client')

    def __init__(self,
                 pokemon_service: PokemonApiService,
                 redis_client: FlaskRedis):
        self.pokemon_service = pokemon_service
        self.redis_client = redis_client

    def execute(self):
        result = self.pokemon_service.fetch_all_pokemons()
        for pokemon in result:
            self.redis_client.set(pokemon.name, pokemon.url)


class SearchPokemonsCommand(PokemonsCommand):
    def execute(self,
                name: Optional[str],
                sort: Sort,
                pagination: Pagination) -> Tuple[List[Pokemon], int]:
        pokemons = self.pokemons_repository.fetch_search(name,
                                                         sort,
                                                         pagination)
        total_count = len(pokemons)
        if pagination.need_count(total_count):
            total_count = self.pokemons_repository.count_search(name)
        else:
            total_count += pagination.offset

        return pokemons, total_count


class CreatePokemonCommand(PokemonsCommand):
    __slots__ = ('pokemon_service', 'redis_client')

    def __init__(self,
                 pokemons_repository: PokemonsRepository,
                 pokemon_service: PokemonApiService,
                 redis_client: FlaskRedis):
        super().__init__(pokemons_repository)
        self.pokemon_service = pokemon_service
        self.redis_client = redis_client

    def execute(self, new_pokemon: Pokemon):
        pokemon = self.pokemons_repository.get_by_name(new_pokemon.name)
        if pokemon:
            return pokemon

        pokemon_url = self.redis_client.get(new_pokemon.name)
        if not pokemon_url:
            raise PokemonNotFoundException

        try:
            external_poke = self.pokemon_service.get_pokemon_by_resource_url(pokemon_url)
            new_pokemon.enrich_from_external_pokemon(external_poke)

            self.pokemons_repository.insert_one(new_pokemon)
            return new_pokemon
        except (PokemonApiException, ExternalPokeApiValidationException):
            raise PokemonExternalServiceException("Problem with external api service")
