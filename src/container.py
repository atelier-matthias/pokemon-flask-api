from containers import BaseContainer
from containers.commands import CommandContainer
from containers.repositories import RepositoryContainer
from containers.services import ServiceContainer


class Container(BaseContainer):
    __slots__ = ('_config', '_ioloop', 'repositories', 'commands', 'services', 'session')

    def __init__(self, app: 'PokemonApp'):
        super().__init__(app)

        self.repositories = RepositoryContainer(self)
        self.commands = CommandContainer(self)
        self.services = ServiceContainer(self)
