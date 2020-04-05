from typing import (
    Any,
    Dict,
)

from commons.errors import invalid_object
from commons.mappers import map_str
from commons.validators import ValidationException
from pokemons.model import (
    Pokemon,
    PokemonSprite,
)


class PokemonSpriteJsonMapper:
    __slots__ = ()

    class Fields:
        __slots__ = ()

        BACK_DEFAULT = 'backDefault'
        BACK_FEMALE = 'backFemale'
        BACK_SHINY = 'backShiny'
        BACK_SHINY_FEMALE = 'backShinyFemale'
        FRONT_DEFAULT = 'frontDefault'
        FRONT_FEMALE = 'frontFemale'
        FRONT_SHINY = 'frontShiny'
        FRONT_SHINY_FEMALE = 'frontShinyFemale'

    @classmethod
    def to_json(cls, pokemon_sprite: PokemonSprite) -> dict:
        _ = cls.Fields

        return {
            _.BACK_DEFAULT: pokemon_sprite.back_default,
            _.BACK_FEMALE: pokemon_sprite.back_female,
            _.BACK_SHINY: pokemon_sprite.back_shiny,
            _.BACK_SHINY_FEMALE: pokemon_sprite.back_shiny_female,
            _.FRONT_DEFAULT: pokemon_sprite.front_default,
            _.FRONT_FEMALE: pokemon_sprite.front_female,
            _.FRONT_SHINY: pokemon_sprite.front_shiny,
            _.FRONT_SHINY_FEMALE: pokemon_sprite.front_shiny_female,
        }


class PokemonJsonMapper:
    __slots__ = ()

    class Fields:
        __slots__ = ()

        ID = 'id'
        NAME = 'name'
        BASE_EXPERIENCE = 'baseExperience'
        HEIGHT = 'height'
        SPRITES = 'sprites'
        WEIGHT = 'weight'
        CREATED_AT = 'createdAt'

    @classmethod
    def from_json(cls, data: Any) -> Pokemon:
        _ = cls.Fields

        if not isinstance(data, dict):
            raise ValidationException.general(invalid_object)

        errors = {}
        name = map_str(data, _.NAME, errors)

        if errors:
            raise ValidationException(errors)

        return Pokemon.new(name)

    @classmethod
    def to_json(cls, pokemon: Pokemon) -> Dict[str, Any]:
        _ = cls.Fields

        return {
            _.ID: pokemon.id,
            _.NAME: pokemon.name,
            _.BASE_EXPERIENCE: pokemon.base_experience,
            _.HEIGHT: pokemon.height,
            _.SPRITES: PokemonSpriteJsonMapper.to_json(pokemon.sprites) if pokemon.sprites else None,
            _.WEIGHT: pokemon.weight,
            _.CREATED_AT: pokemon.created_at
        }
