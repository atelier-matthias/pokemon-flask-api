from typing import (
    Any,
    Dict,
)
from uuid import UUID

from commons.errors import invalid_object
from commons.mappers import map_str
from commons.validators import ValidationException
from encounters.model import Encounter


class EncounterJsonMapper:
    __slots__ = ()

    class Fields:
        __slots__ = ()

        ID = 'id'
        PLACE = 'place'
        NOTE = 'note'
        POKEMON_ID = 'pokemonId'
        TIMESTAMP = 'timestamp'

    @classmethod
    def from_json(cls, data: Any, pokemon_id: UUID) -> Encounter:
        _ = cls.Fields

        if not isinstance(data, dict):
            raise ValidationException.general(invalid_object)

        errors = {}
        place = map_str(data, _.PLACE, errors)
        note = map_str(data, _.NOTE, errors, required=False)

        if errors:
            raise ValidationException(errors)

        return Encounter.new(place, note, pokemon_id)

    @classmethod
    def to_json(cls, encounter: Encounter) -> Dict[str, Any]:
        _ = cls.Fields

        return {
            _.ID: encounter.id,
            _.PLACE: encounter.place,
            _.NOTE: encounter.note,
            _.TIMESTAMP: encounter.timestamp
        }
