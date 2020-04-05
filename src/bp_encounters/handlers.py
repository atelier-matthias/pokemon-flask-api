from flask import (
    Blueprint,
    request,
)
from werkzeug.exceptions import (
    Conflict,
    NotFound,
)

from app import app
from bp_encounters.request_mapper import EncounterJsonMapper
from commons.query import QueryParams
from commons.request_methods import RequestMethods
from commons.responses import response_ok
from commons.validators import ValidationException
from pokemons.commands import (
    PokemonNotFoundException,
)

encounters_page = Blueprint('encounters_page', __name__)
GET_AVAILABLE_SORT = {EncounterJsonMapper.Fields.TIMESTAMP,
                      EncounterJsonMapper.Fields.PLACE}
DEFAULT_ORDER = EncounterJsonMapper.Fields.TIMESTAMP
DEFAULT_DIRECTION = 'asc'
MIN_SEARCH_LEN = 3
DEFAULT_PAGE_SIZE = 25
MAX_PAGE_SIZE = 50


@encounters_page.route(f'/pokemons/<uuid:pokemon_id>/encounters', methods=[RequestMethods.GET])
def list_pokemons(pokemon_id):
    _ = app.container.commands
    _F = EncounterJsonMapper.Fields
    search_encounters_command = _.search_encounters
    query_params = QueryParams.search(request,
                                      available_sort=GET_AVAILABLE_SORT,
                                      default_sort_field=DEFAULT_ORDER,
                                      default_sort_order=DEFAULT_DIRECTION,
                                      default_limit=DEFAULT_PAGE_SIZE,
                                      max_limit=MAX_PAGE_SIZE)

    note = query_params.get_arg(_F.NOTE)
    place = query_params.get_arg(_F.PLACE)

    pokemons, total_count = search_encounters_command.execute(place,
                                                              note,
                                                              pokemon_id,
                                                              query_params.get_sort(),
                                                              query_params.get_pagination())

    return response_ok({
        "encounters": [EncounterJsonMapper.to_json(item) for item in pokemons],
        "totalCount": total_count
    })


@encounters_page.route('/pokemons/<uuid:pokemon_id>/encounters', methods=[RequestMethods.POST])
def create_pokemon(pokemon_id):
    _ = app.container.commands
    create_encounter_command = _.create_encounter

    try:
        json_body = request.json
        encounter = EncounterJsonMapper.from_json(json_body, pokemon_id)
        encounter = create_encounter_command.execute(encounter)
        return response_ok({
            "encounter": EncounterJsonMapper.to_json(encounter)
        })
    except ValidationException as exception:
        raise Conflict(exception.parameters)
    except PokemonNotFoundException as exception:
        raise NotFound(exception)
