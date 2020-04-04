from datetime import datetime
from typing import Optional
from uuid import (
    UUID,
    uuid4,
)


class PokemonSprite:
    __slots__ = ('back_default', 'back_female', 'back_shiny', 'back_shiny_female', 'front_default', 'front_female', 'front_shiny', 'front_shiny_female')

    back_default: Optional[str]
    back_female: Optional[str]
    back_shiny: Optional[str]
    back_shiny_female: Optional[str]
    front_default: Optional[str]
    front_female: Optional[str]
    front_shiny: Optional[str]
    front_shiny_female: Optional[str]

    def __init__(self,
                 back_default: Optional[str],
                 back_female: Optional[str],
                 back_shiny: Optional[str],
                 back_shiny_female: Optional[str],
                 front_default: Optional[str],
                 front_female: Optional[str],
                 front_shiny: Optional[str],
                 front_shiny_female: Optional[str]):
        self.back_default = back_default
        self.back_female = back_female
        self.back_shiny = back_shiny
        self.back_shiny_female = back_shiny_female
        self.front_default = front_default
        self.front_female = front_female
        self.front_shiny = front_shiny
        self.front_shiny_female = front_shiny_female


class ExternalPokemon:
    __slots__ = ('name', 'base_experience', 'height', 'sprites', 'weight')

    name: str
    base_experience: Optional[int]
    height: Optional[int]
    sprites: Optional[PokemonSprite]
    weight: Optional[int]

    def __init__(self,
                 name: str,
                 base_experience: Optional[int],
                 height: Optional[int],
                 sprites: Optional[PokemonSprite],
                 weight: Optional[int]):
        self.name = name
        self.base_experience = base_experience
        self.height = height
        self.sprites = sprites
        self.weight = weight


class Pokemon:
    __slots__ = ('id', 'name', 'base_experience', 'height', 'sprites', 'weight', 'created_at')

    id: UUID
    name: str
    base_experience: Optional[int]
    height: Optional[int]
    sprites: Optional[PokemonSprite]
    weight: Optional[int]
    created_at: datetime

    def __init__(self,
                 id: UUID,
                 name: str,
                 base_experience: Optional[int],
                 height: Optional[int],
                 sprites: Optional[PokemonSprite],
                 weight: Optional[int],
                 created_at: datetime):
        self.id = id
        self.name = name
        self.base_experience = base_experience
        self.height = height
        self.sprites = sprites
        self.weight = weight
        self.created_at = created_at

    @classmethod
    def new(cls,
            name: str):
        obj = cls(uuid4(),
                  name,
                  base_experience=None,
                  height=None,
                  sprites=None,
                  weight=None,
                  created_at=datetime.utcnow())

        return obj

    def enrich_from_external_pokemon(self, external_poke: ExternalPokemon):
        self.base_experience = external_poke.base_experience
        self.height = external_poke.height
        self.sprites = external_poke.sprites
        self.weight = external_poke.weight


class PokemonRedis:
    __slots__ = ('name', 'url')

    name: str
    url: str

    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url
