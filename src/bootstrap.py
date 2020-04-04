from typing import (
    Dict,
    Type,
)

from config import BaseConfig


def starter(env_map: Dict[str, Type[BaseConfig]], description: str = "Pokemon Application Rest Api") -> BaseConfig:
    from os import (
        environ,
    )
    from argparse import ArgumentParser

    parser = ArgumentParser(description=description)
    parser.add_argument('-c', default='dev', dest='config', help='Server configuration file')
    parser.add_argument('-b', default=None, dest='base_path', help='Base path')

    cmd_args = parser.parse_args()

    env = (environ.get('ENVIRONMENT') if environ.get('ENVIRONMENT') else cmd_args.config).lower()

    config = env_map.get(env.lower(), env_map.get('default'))()

    if cmd_args.base_path:
        config.BASE_PATH = cmd_args.base_path

    print(f'Starting with {env}')
    print(f'Base path = {config.BASE_PATH}')

    return config
