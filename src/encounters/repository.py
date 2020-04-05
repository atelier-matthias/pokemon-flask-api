from typing import (
    Optional,
    List,
)
from uuid import UUID

from commons.commands import (
    Sort,
    Pagination,
)
from commons.mongo import MongoRepository
from commons.mongo_utils import MongoUtils
from encounters.mappers import EncounterMongoMapper
from encounters.model import Encounter
from encounters.sort_mapper import EncounterSortMongoMapper


class EncountersRepository(MongoRepository):

    @classmethod
    def get_collection_name(cls) -> str:
        return 'encounters'

    def insert_one(self, encounter: Encounter):
        self.collection.insert_one(EncounterMongoMapper.to_mongo(encounter))

    def fetch_search(self,
                     place: Optional[str],
                     note: Optional[str],
                     pokemon_id: Optional[UUID],
                     sort: Sort,
                     pagination: Pagination) -> List[Encounter]:
        _ = EncounterMongoMapper.Fields
        query = {}

        if place:
            query[_.PLACE] = MongoUtils.match_string_contains(place)

        if note:
            query[_.NOTE] = MongoUtils.match_string_contains(note)

        if pokemon_id:
            query[_.POKEMON_ID] = pokemon_id

        cursor = self.collection.find(query,
                                      limit=pagination.limit,
                                      skip=pagination.offset,
                                      sort=EncounterSortMongoMapper.to_mongo([sort]))

        return [EncounterMongoMapper.from_mongo(item) for item in cursor]

    def count_search(self,
                     place: Optional[str],
                     note: Optional[str],
                     pokemon_id: Optional[UUID]) -> int:
        _ = EncounterMongoMapper.Fields
        query = {}

        if place:
            query[_.PLACE] = MongoUtils.match_string_contains(place)

        if note:
            query[_.NOTE] = MongoUtils.match_string_contains(note)

        if pokemon_id:
            query[_.POKEMON_ID] = pokemon_id

        counter = self.collection.count_documents(query)

        return counter
