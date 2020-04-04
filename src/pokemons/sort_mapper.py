from typing import (
    Dict,
    List,
    Tuple,
)

import pymongo

from commons.commands import Sort
from pokemons.mappers import PokemonMongoMapper
from pokemons.request_mapper import PokemonJsonMapper


class PokemonSortMongoMapper:
    mongo = PokemonMongoMapper.Fields
    json = PokemonJsonMapper.Fields

    TO_MONGO = {
        json.NAME: mongo.NAME,
        json.CREATED_AT: mongo.CREATED_AT
    }

    direction: Dict[str, int] = {
        'asc': pymongo.ASCENDING,
        'desc': pymongo.DESCENDING
    }

    @classmethod
    def to_mongo(cls, sorts: List[Sort]) -> List[Tuple[str, int]]:
        if sorts:
            return [(cls.TO_MONGO[sort.field], cls.direction[sort.direction]) for sort in sorts]
        else:
            return []
