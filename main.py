import click

from mymodule import docker_class
from mymodule import dock_lib

global_host = ""


@click.group()
@click.option("--host", envvar="DOCKER_HOST", help="Specify docker host or use available environment variable")
def cli(host):
    global global_host
    global_host = host
    if not dock_lib.check_docker(host):
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
def init(install, update, test):
    """
    Creates the container and initializes `dock-runner-init.json` file.
    """
    # opts = {
    #     "install": install,
    #     "update": update,
    #     "test": test
    # }
    # write_to_file(opts)
    click.echo("Creating dock-runner-init.json file ...")
    with docker_class.open_init_file() as data:
        data.clear()
        data.install_command = install
        data.update_command = update
        data.test_command = test
    init_file()


# @cli.command("init-file")
def init_file():
    host = global_host
    with docker_class.open_init_file() as data:
        click.echo("Pulling ubuntu:xenial Image ...")
        dock_lib.pull_image(host)
        click.echo("Creating test machine image. Installing packages, setting up environment. May take time ...")
        image, install_logs = dock_lib.create_image(host, data.install_command)
        data.image = image.tags[0]
        data.install_logs = install_logs

    click.echo("Image created : {}".format(image.tags[0]))
