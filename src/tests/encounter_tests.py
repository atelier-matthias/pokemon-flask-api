from flask import Response

from tests.base import BaseRestTestCase


class EncountersTests(BaseRestTestCase):

    def test_api(self):
        result = self.app.get('/')
        assert isinstance(result, Response)

    def test_create_encounter_expect_success(self):
        json_body = {
            "name": "bulbasaur"
        }

        result = self.make_api_post('/pokemons', json_body)
        assert result['status'] == 'OK'
        pokemon_id = result['pokemon']['id']

        json_body = {
            "place": "forrest"
        }
        result = self.make_api_post(f'/pokemons/{pokemon_id}/encounters', json_body)
        assert result['status'] == 'OK'
