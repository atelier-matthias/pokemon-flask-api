from http import HTTPStatus

from flask import Response

from tests.base import BaseRestTestCase


class PokemonsTests(BaseRestTestCase):

    def test_api(self):
        result = self.app.get('/')
        assert isinstance(result, Response)

    def test_pokemons_list_expect_success(self):
        result = self.make_api_get('/pokemons')
        assert result['status'] == 'OK'

    def test_create_pokemon_expect_success(self):
        json_body = {
            "name": "bulbasaur"
        }

        result = self.make_api_post('/pokemons', json_body)
        assert result['status'] == 'OK'

    def test_create_pokemon_validation_exception(self):
        with self.subTest('NAME field required'):
            json_body = {
                "name": None
            }

            result = self.make_api_post('/pokemons', json_body, expected_status=HTTPStatus.CONFLICT)
            assert result['status'] == 'Conflict'

        with self.subTest('NAME field required'):
            json_body = {
            }

            result = self.make_api_post('/pokemons', json_body, expected_status=HTTPStatus.CONFLICT)
            assert result['status'] == 'Conflict'

        with self.subTest('NAME field is not String'):
            json_body = {
                "name": 1
            }

            result = self.make_api_post('/pokemons', json_body, expected_status=HTTPStatus.CONFLICT)
            assert result['status'] == 'Conflict'
            details_code = result['details']['name']['code']
            assert details_code == 'INVALID_KIND'

            json_body = {
                "name": ['name']
            }

            result = self.make_api_post('/pokemons', json_body, expected_status=HTTPStatus.CONFLICT)
            assert result['status'] == 'Conflict'
            details_code = result['details']['name']['code']
            assert details_code == 'INVALID_KIND'
