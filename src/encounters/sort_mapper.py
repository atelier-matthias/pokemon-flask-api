from typing import (
    Dict,
    List,
    Tuple,
)

import pymongo

from bp_encounters.request_mapper import EncounterJsonMapper
from commons.commands import Sort
from encounters.mappers import EncounterMongoMapper


class EncounterSortMongoMapper:
    mongo = EncounterMongoMapper.Fields
    json = EncounterJsonMapper.Fields

    TO_MONGO = {
        json.PLACE: mongo.PLACE,
        json.TIMESTAMP: mongo.TIMESTAMP
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
