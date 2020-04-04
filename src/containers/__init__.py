
class BaseContainer:
    __slots__ = ('_app',)

    def __init__(self, app):
        self._app = app

    @property
    def app(self) -> 'PokemonApp':
        return self._app


class SubContainer:
    __slots__ = ('_parent',)

    def __init__(self, parent: 'Container') -> None:
        super().__init__()
        self._parent = parent


# noinspection PyPep8Naming
class cached_property:
    __slots__ = ('_constructor', '_name')

    def __init__(self, constructor):
        self._constructor = constructor
        self._name = f"_{constructor.__name__}"

    def __get__(self, container, instance):
        instance = container.__dict__.get(self._name)
        if instance is None:
            instance = self._constructor(container)
            container.__dict__[self._name] = instance
        return instance
