import json
from http import HTTPStatus
from unittest import TestCase

from flask import Response

from app import PokemonApp
from config import TestsConfig


class BaseRestTestCase(TestCase):
    def get_config(self):
        return TestsConfig()

    def setUp(self) -> None:
        from bp_pokemon.handlers import pokemon_page
        from bp_encounters.handlers import encounters_page
        flask_app = PokemonApp(__name__)
        flask_app.config.from_object(self.get_config())

        flask_app.register_blueprint(pokemon_page)
        flask_app.register_blueprint(encounters_page)
        flask_app.register_errors_handlers()
        flask_app.init_redis()
        self.app = flask_app
        self.app = self.app.test_client()

    def tearDown(self) -> None:
        self.app.application.container.repositories.mongo_connection.db.client.drop_database(self.get_config().DB_NAME)

    def make_api_get(self, url: str, expected_status: int = HTTPStatus.OK):
        result = self.app.get(url, content_type='application/json')
        assert isinstance(result, Response)
        assert result.status_code == expected_status

        return json.loads(result.data)

    def make_api_post(self,
                      url: str,
                      json_body: dict,
                      expected_status: int = HTTPStatus.OK):
        result = self.app.post(url,
                               data=json.dumps(json_body),
                               content_type='application/json')
        assert isinstance(result, Response)
        assert result.status_code == expected_status

        return json.loads(result.data)
