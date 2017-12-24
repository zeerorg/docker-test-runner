import docker
import click

from docker.errors import DockerException


@click.command()
@click.option("--host", envvar="DOCKER_HOST", help="Specify docker host or use available environment variable")
def cli(host):
    try:
        if not docker.DockerClient(base_url=host).ping():
            raise DockerException
    except (NameError, DockerException):
        click.echo("No docker installed, or host not correct.\nSee dock-runner --help")
        return
