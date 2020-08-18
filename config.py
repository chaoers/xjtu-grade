
import os
import pathlib
from pathlib import Path

import toml

CONFIG_EXAMPLE = 'config.example.toml'
CONFIG_FILE = 'config.toml'


def load_config() -> None:
    if not Path(CONFIG_FILE).exists():
        print(f'No config file detected using default config.')
        print(f'Using the default config.')
        src: Path = Path(CONFIG_EXAMPLE)
        dst: Path = Path(CONFIG_FILE)
        dst.write_bytes(src.read_bytes())

    with open(CONFIG_FILE, encoding='utf8') as f:
        config: dict = toml.load(f)

    if config['USER']['NETID'] == 'PLEASE INPUT YOUR NETID':
        print(f'Please input your netid:', end='')
        netid: str = input().strip()
        print(f'Please input your password:', end='')
        password: str = input().strip()
        config['USER']['NETID'] = netid
        config['USER']['PASSWORD'] = password
        with open(CONFIG_FILE, 'w', encoding='utf8') as f:
            toml.dump(config, f)

    return config


class Config:
    def __init__(self) -> None:
        config = load_config()

        self.net_id = config['USER']['NETID']
        self.password = config['USER']['PASSWORD']

        self.public_key = config['WEB']['PUBLIC_KEY']


config = Config()
