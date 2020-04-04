import json
from http import HTTPStatus
from typing import List

import pokebase
import requests

from pokemons.mappers import (
    PokemonRedisMapper,
    ExternalPokemonMapper,
)
from pokemons.model import (
    PokemonRedis,
    ExternalPokemon,
)


class PokemonApiException(Exception):
    __slots__ = ()


class PokemonApiService:
    __slots__ = ('api_url', 'pokemon_client')
    FETCH_LIST = "pokemon"

    def __init__(self,
                 base_external_url: str):
        self.api_url = base_external_url
        self.pokemon_client = pokebase

    def get_pokemon_by_resource_url(self, url: str) -> ExternalPokemon:
        result = requests.get(url)
        if result.status_code != HTTPStatus.OK:
            raise PokemonApiException
        result = json.loads(result.content)
        return ExternalPokemonMapper.from_service(result)

    def fetch_all_pokemons(self) -> List[PokemonRedis]:
        URL = '/'.join((self.api_url, self.FETCH_LIST))
        PARAMS = 'limit=1000'

        result = requests.get(url=URL, params=PARAMS)
        if result.status_code != HTTPStatus.OK:
            raise PokemonApiException

        try:
            result = json.loads(result.content)
            pokemons = [PokemonRedisMapper.from_name_url(item['name'],
                                                         item['url']) for item in result['results']]
            return pokemons
        except:
            raise PokemonApiException
