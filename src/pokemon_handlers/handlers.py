from flask import (
    Blueprint,
    request,
)
from werkzeug.exceptions import (
    Conflict,
)

from commons.query import QueryParams
from commons.request_methods import RequestMethods
from commons.responses import response_ok
from commons.validators import ValidationException
from pokemons.request_mapper import PokemonJsonMapper

pokemon_page = Blueprint('pokemon_page', __name__)
GET_AVAILABLE_SORT = {PokemonJsonMapper.Fields.CREATED_AT}
DEFAULT_ORDER = PokemonJsonMapper.Fields.CREATED_AT
DEFAULT_DIRECTION = 'asc'
MIN_SEARCH_LEN = 3
DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 50

from app import app


@pokemon_page.route('/pokemons', methods=[RequestMethods.GET])
def get_pokemons():
    _ = app.container.commands
    _F = PokemonJsonMapper.Fields

    try:
        fetch_pokemons_command = _.fetch_pokemons
        query_params = QueryParams.search(request,
                                          available_sort=GET_AVAILABLE_SORT,
                                          default_sort_field=DEFAULT_ORDER,
                                          default_sort_order=DEFAULT_DIRECTION,
                                          default_limit=DEFAULT_PAGE_SIZE,
                                          max_limit=MAX_PAGE_SIZE)

        name = query_params.get_arg(_F.NAME)

        pokemons, total_count = fetch_pokemons_command.execute(name,
                                                               query_params.get_sort(),
                                                               query_params.get_pagination())

        return response_ok({
            "pokemons": [PokemonJsonMapper.to_json(item) for item in pokemons],
            "totalCount": total_count
        })
    except ValidationException as exception:
        raise Conflict(exception.parameters)


@pokemon_page.route('/pokemons', methods=[RequestMethods.POST])
def add_pokemon():
    _ = app.container.commands
    _F = PokemonJsonMapper.Fields

    try:
        create_pokemon_command = _.create_pokemon

        json_body = request.json
        pokemon = PokemonJsonMapper.from_json(json_body)
        result = create_pokemon_command.execute(pokemon)

        return response_ok({
            "pokemon": PokemonJsonMapper.to_json(result)
        })
    except ValidationException as exception:
        raise Conflict(exception.parameters)
