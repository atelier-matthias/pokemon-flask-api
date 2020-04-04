from flask_pymongo import PyMongo
from containers import (
    SubContainer,
    BaseContainer,
    cached_property,
)
from pokemons.repository import PokemonsRepository


class RepositoryContainer(SubContainer):

    def __init__(self, parent: BaseContainer) -> None:
        super().__init__(parent)

    @cached_property
    def mongo_connection(self) -> PyMongo:
        client = PyMongo(self._parent.app)
        return client

    @cached_property
    def pokemons(self) -> PokemonsRepository:
        return PokemonsRepository(self.mongo_connection)
