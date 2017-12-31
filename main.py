import click

from .dock_lib import *
from .docker_class import open_init_file


@click.group()
@click.option("--host", envvar="DOCKER_HOST", help="Specify docker host or use available environment variable")
@click.pass_context
def cli(ctx, host):
    ctx.obj['host'] = host
    if not check_docker(host):
        click.echo("No docker installed, or host not correct.\nSee dock-runner --help")
        return


@cli.command()
@click.option("--install", prompt=True, help="Specify install commands for ubuntu installation. These are run first "
                                             "time to create a docker image. Expected: Install base dependencies.")
@click.option("--update", prompt=True, help="Specify commands which update the test environment every time they are "
                                            "run. These are run to fetch the newest code changes. These may or may "
                                            "not be persisted.")
@click.option("--test", prompt=True, help="Specify test commands which run the test. The output of these commands is "
                                          "logged on terminal.")
@click.pass_context
def init(ctx, install, update, test):
    """
    Creates the container and initializes `dock-runner-init.json` file.
    """
    # opts = {
    #     "install": install,
    #     "update": update,
    #     "test": test
    # }
    # write_to_file(opts)
    # init_file(ctx)
    with open_init_file() as data:
        data.clear()
        data.install_command = install
        data.update_command = update
        data.test_command = test


@cli.command("init-file")
@click.pass_context
def init_file(ctx):
    host = ctx.obj['host']
    with open_init_file() as data:
        pull_image(host)
        image, install_logs = create_image(host, data.install_command)
        data.image = image.tags[0]
        data.install_logs = install_logs
