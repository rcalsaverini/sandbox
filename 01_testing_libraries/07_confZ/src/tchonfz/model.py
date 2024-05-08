import click
from confz import FileSource
from tchonfz.config import AvatarConfig
from pprint import pprint

config = AvatarConfig(config_sources=FileSource("config.yaml"))


@click.group()
def model():
    pass


@model.command()
def train():
    print("Training model")
    pprint(config.training)


@model.command()
def scoring():
    print("Scoring model")


if __name__ == "__main__":
    model()
