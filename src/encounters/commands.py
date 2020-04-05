from typing import (
    Tuple,
    List,
    Optional,
)
from uuid import UUID

from commons.commands import (
    Sort,
    Pagination,
)
from encounters.model import Encounter
from encounters.repository import EncountersRepository
from pokemons.commands import PokemonNotFoundException
from pokemons.repository import PokemonsRepository


class EncounterCommand:
    __slots__ = ('encounters_repository',)

    def __init__(self, encounters_repository: EncountersRepository):
        self.encounters_repository = encounters_repository


class CreateEncounterCommand(EncounterCommand):
    __slots__ = ('encounters_repository', 'pokemons_repository')

    def __init__(self,
                 encounters_repository: EncountersRepository,
                 pokemons_repository: PokemonsRepository):
        super().__init__(encounters_repository)
        self.pokemons_repository = pokemons_repository

    def execute(self, encounter: Encounter) -> Encounter:
        pokemon = self.pokemons_repository.get_by_id(encounter.pokemon_id)
        if not pokemon:
            raise PokemonNotFoundException

        self.encounters_repository.insert_one(encounter)
        return encounter


class SearchEncounterCommand(EncounterCommand):
    def execute(self,
                place: Optional[str],
                note: Optional[str],
                pokemon_id: Optional[UUID],
                sort: Sort,
                pagination: Pagination) -> Tuple[List[Encounter], int]:
        encounters = self.encounters_repository.fetch_search(place,
                                                             note,
                                                             pokemon_id,
                                                             sort,
                                                             pagination)
        total_count = len(encounters)
        if pagination.need_count(total_count):
            total_count = self.encounters_repository.count_search(place, note, pokemon_id)
        else:
            total_count += pagination.offset

        return encounters, total_count
