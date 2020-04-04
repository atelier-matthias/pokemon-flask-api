from typing import (
    Any,
    Tuple,
    Dict,
)

from commons.mappers import (
    map_str,
    map_int,
)
from pokemons.model import (
    Pokemon,
    PokemonRedis,
    PokemonSprite,
    ExternalPokemon,
)


class ExternalPokeApiValidationException(Exception):
    __slots__ = ()


class PokemonSpriteMongoMapper:
    __slots__ = ()

    class Fields:
        __slots__ = ()

        BACK_DEFAULT = 'back_default'
        BACK_FEMALE = 'back_female'
        BACK_SHINY = 'back_shiny'
        BACK_SHINY_FEMALE = 'back_shiny_female'
        FRONT_DEFAULT = 'front_default'
        FRONT_FEMALE = 'front_female'
        FRONT_SHINY = 'front_shiny'
        FRONT_SHINY_FEMALE = 'front_shiny_female'

    @classmethod
    def from_mongo(cls, data: dict) -> PokemonSprite:
        _ = cls.Fields

        return PokemonSprite(data[_.BACK_DEFAULT],
                             data[_.BACK_FEMALE],
                             data[_.BACK_SHINY],
                             data[_.BACK_SHINY_FEMALE],
                             data[_.FRONT_DEFAULT],
                             data[_.FRONT_FEMALE],
                             data[_.FRONT_SHINY],
                             data[_.FRONT_SHINY_FEMALE])

    @classmethod
    def to_mongo(cls, pokemon_sprite: PokemonSprite) -> dict:
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

    @classmethod
    def from_external_service(cls, data: Dict[str, Any]) -> PokemonSprite:
        _ = cls.Fields

        if not isinstance(data, dict):
            raise ExternalPokeApiValidationException

        errors = {}

        back_default = map_str(data, _.BACK_DEFAULT, errors, required=False)
        back_female = map_str(data, _.BACK_FEMALE, errors, required=False)
        back_shiny = map_str(data, _.BACK_SHINY, errors, required=False)
        back_shiny_female = map_str(data, _.BACK_SHINY_FEMALE, errors, required=False)
        front_default = map_str(data, _.FRONT_DEFAULT, errors, required=False)
        front_female = map_str(data, _.FRONT_FEMALE, errors, required=False)
        front_shiny = map_str(data, _.FRONT_SHINY, errors, required=False)
        front_shiny_female = map_str(data, _.FRONT_SHINY_FEMALE, errors, required=False)

        if errors:
            raise ExternalPokeApiValidationException(errors)

        return PokemonSprite(back_default,
                             back_female,
                             back_shiny,
                             back_shiny_female,
                             front_default,
                             front_female,
                             front_shiny,
                             front_shiny_female)


class PokemonMongoMapper:
    __slots__ = ()

    class Fields:
        __slots__ = ()

        ID = '_id'
        NAME = 'name'
        BASE_EXPERIENCE = 'base_experience'
        HEIGHT = 'height'
        SPRITES = 'sprites'
        WEIGHT = 'weight'
        CREATED_AT = 'created_at'

    @classmethod
    def from_mongo(cls, data: Any) -> Pokemon:
        _ = cls.Fields

        return Pokemon(data[_.ID],
                       data[_.NAME],
                       data[_.BASE_EXPERIENCE],
                       data[_.HEIGHT],
                       PokemonSpriteMongoMapper.from_mongo(data[_.SPRITES]),
                       data[_.WEIGHT],
                       data[_.CREATED_AT])

    @classmethod
    def to_mongo(cls, pokemon: Pokemon) -> dict:
        _ = cls.Fields

        return {
            _.ID: pokemon.id,
            _.NAME: pokemon.name,
            _.BASE_EXPERIENCE: pokemon.base_experience,
            _.HEIGHT: pokemon.height,
            _.SPRITES: PokemonSpriteMongoMapper.to_mongo(pokemon.sprites),
            _.WEIGHT: pokemon.weight,
            _.CREATED_AT: pokemon.created_at
        }


class PokemonRedisMapper:
    __slots__ = ()

    class Fields:
        __slots__ = ()

        NAME = 'name'
        URL = 'url'

    @classmethod
    def to_redis(cls, pokemon: PokemonRedis) -> Tuple[str, str]:
        _ = cls.Fields

        return pokemon.name, pokemon.url

    @classmethod
    def from_name_url(cls, name: str, url: str) -> PokemonRedis:
        _ = cls.Fields

        return PokemonRedis(name, url)


class ExternalPokemonMapper:
    __slots__ = ()

    class Fields:
        __slots__ = ()
        NAME = 'name'
        BASE_EXPERIENCE = 'base_experience'
        HEIGHT = 'height'
        SPRITES = 'sprites'
        WEIGHT = 'weight'

    @classmethod
    def from_service(cls, data: Dict[str, Any]) -> ExternalPokemon:
        _ = cls.Fields
        if not isinstance(data, dict):
            raise ExternalPokeApiValidationException

        errors = {}

        name = map_str(data, _.NAME, errors)
        base_experience = map_int(data, _.BASE_EXPERIENCE, errors)
        height = map_int(data, _.HEIGHT, errors)
        sprites = PokemonSpriteMongoMapper.from_external_service(data.get(_.SPRITES))
        weight = map_int(data, _.WEIGHT, errors)

        if errors:
            raise ExternalPokeApiValidationException(errors)

        return ExternalPokemon(name,
                               base_experience,
                               height,
                               sprites,
                               weight)
