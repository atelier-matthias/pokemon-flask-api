from datetime import datetime

from flask import (
    Flask,
)

from commons.exceptions import error_handlers_map
from config import (
    ENV_MAP,
)
from bootstrap import starter
from container import Container
from pokemon_handlers.handlers import pokemon_page


class PokemonApp(Flask):
    start_date: datetime

    def __init__(self, name: str):
        super().__init__(name)
        self.container = Container(self)
        self.start_date = datetime.utcnow()
        self._services = []

    def build(self):
        self.register_blueprint(pokemon_page)
        self.register_errors_handlers()
        self.init_redis()
        return self

    def init_redis(self):
        self.container.services.redis_client.init_app(self)
        self._init_redis_data()

    def _init_redis_data(self):
        self.container.commands.initialize_redis_pokemon_data.execute()

    def register_errors_handlers(self):
        for code, handler in error_handlers_map.items():
            self.register_error_handler(code, handler)


app = PokemonApp(__name__)
config = starter(ENV_MAP)
app.config.from_object(config)


if __name__ == '__main__':
    app.build().run()
