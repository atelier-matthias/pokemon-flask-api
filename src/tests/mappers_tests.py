from unittest import TestCase

from bp_pokemon.request_mapper import PokemonJsonMapper
from pokemons.model import Pokemon


class MappersTests(TestCase):
    def test_pokemon_json_mapper(self):
        json_body = {
            "name": "some pokemon name"
        }
        pokemon = PokemonJsonMapper.from_json(json_body)
        assert isinstance(pokemon, Pokemon)

        assert pokemon.name == json_body['name']
