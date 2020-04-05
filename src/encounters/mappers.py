from typing import Any

from encounters.model import Encounter


class EncounterMongoMapper:
    __slots__ = ()

    class Fields:
        __slots__ = ()

        ID = '_id'
        PLACE = 'place'
        NOTE = 'note'
        POKEMON_ID = 'pokemon_id'
        TIMESTAMP = 'timestamp'

    @classmethod
    def to_mongo(cls, encounter: Encounter) -> dict:
        _ = cls.Fields

        return {
            _.ID: encounter.id,
            _.PLACE: encounter.place,
            _.NOTE: encounter.note,
            _.POKEMON_ID: encounter.pokemon_id,
            _.TIMESTAMP: encounter.timestamp
        }

    @classmethod
    def from_mongo(cls, data: dict) -> Encounter:
        _ = cls.Fields

        return Encounter(data[_.ID],
                         data[_.PLACE],
                         data[_.NOTE],
                         data[_.POKEMON_ID],
                         data[_.TIMESTAMP])
