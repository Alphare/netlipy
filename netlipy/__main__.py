#!/usr/bin/env python3
from pathlib import Path

import click

from netlipy.server import Netlipy

@click.command()
@click.argument('root_dir')
@click.option('--host', default='0.0.0.0')
@click.option('--port', default='8000')
def main(root_dir, host, port):
    path = Path(root_dir).absolute()

    if not path.exists():
        raise ValueError(f"root_dir ({path}) does not exist.")

    netlipy = Netlipy(root_dir=path, host=host, port=port)
    netlipy.serve()