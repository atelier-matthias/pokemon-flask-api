from typing import Optional
from uuid import (
    UUID,
    uuid4,
)

from commons.helpers import get_unixtimestamp


class Encounter:
    __slots__ = ('id', 'place', 'note', 'pokemon_id', 'timestamp')

    id: UUID
    place: str
    note: Optional[str]
    pokemon_id: UUID
    timestamp: int

    def __init__(self,
                 id: UUID,
                 place: str,
                 note: Optional[str],
                 pokemon_id: UUID,
                 timestamp: int):
        self.id = id
        self.place = place
        self.note = note
        self.pokemon_id = pokemon_id
        self.timestamp = timestamp

    @classmethod
    def new(cls, place: str, note: Optional[str], pokemon_id: UUID):
        obj = cls(uuid4(),
                  place,
                  note,
                  pokemon_id,
                  get_unixtimestamp())

        return obj
