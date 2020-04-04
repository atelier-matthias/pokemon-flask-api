from typing import (
    Optional,
    List,
)

from commons.commands import (
    Sort,
    Pagination,
)
from commons.mongo import MongoRepository
from commons.mongo_utils import MongoUtils
from pokemons.mappers import PokemonMongoMapper
from pokemons.model import Pokemon
from pokemons.sort_mapper import PokemonSortMongoMapper


class PokemonsRepository(MongoRepository):

    @classmethod
    def get_collection_name(cls) -> str:
        return 'pokemons'

    def fetch_search(self,
                     name: Optional[str],
                     sort: Sort,
                     pagination: Pagination
                     ) -> List[Pokemon]:
        _ = PokemonMongoMapper.Fields
        query = {}

        if name:
            query[_.NAME] = MongoUtils.match_string_contains(name)

        cursor = self.collection.find(query,
                                      limit=pagination.limit,
                                      skip=pagination.offset,
                                      sort=PokemonSortMongoMapper.to_mongo([sort]))

        return [PokemonMongoMapper.from_mongo(item) for item in cursor]

    def count_search(self, name: Optional[str]) -> int:
        _ = PokemonMongoMapper.Fields
        query = {}

        if name:
            query[_.NAME] = MongoUtils.match_string_contains(name)

        counter = self.collection.count_documents(query)

        return counter

    def insert_one(self, pokemon: Pokemon):
        self.collection.insert_one(PokemonMongoMapper.to_mongo(pokemon))

    def get_by_name(self, name: str) -> Optional[Pokemon]:
        _ = PokemonMongoMapper.Fields

        query = {
            _.NAME: name
        }

        result = self.collection.find_one(query)
        if result:
            return PokemonMongoMapper.from_mongo(result)
