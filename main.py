import click

from mymodule import docker_class
from mymodule.dock_lib import CallDocker

global_host = ""


@click.group()
@click.option("--host", envvar="DOCKER_HOST", help="Specify docker host or use available environment variable")
def cli(host):
    global global_host
    global_host = host
    if not CallDocker.check_docker(host):
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
    click.echo("Creating dock-runner-init.json file ...")
    with docker_class.open_init_file() as data:
        data.clear()
        data.install_command = install
        data.update_command = update
        data.test_command = test
    init_file()


@cli.command("init-file", help="Create container from init.json file")
def init_file():
    host = global_host
    dock_worker = CallDocker(host)
    with docker_class.open_init_file() as data:
        click.echo("Pulling ubuntu:xenial Image ...")
        dock_worker.pull_image()
        click.echo("Creating test machine image. Installing packages, setting up environment. May take time ...")
        data.image, data.install_container = dock_worker.create_test_image(data.install_command)
        click.echo("Image created : {}".format(data.image))


@cli.command("test", help="Runs the test container")
def test() -> None:
    """
    Steps to run test container

    1. Delete update container, update image and test container
    2. Create update container from install image
    3. Create update image from update container
    4. Use update image to create test container

    """
    host = global_host
    dock_worker = CallDocker(host)
    with docker_class.open_init_file() as data:
        if data.update_container:
            dock_worker.del_container(data.update_container)
        if data.test_container:
            dock_worker.del_container(data.test_container)
        if data.update_image:
            dock_worker.del_image(data.update_container)

        click.echo("Creating container from image {}".format(data.image))
        data.update_image, data.update_container = dock_worker.create_update_container(data.image, data.update_command)
        click.echo("Running test")
        data.test_container = dock_worker.run_test_container(data.update_image, data.test_command)
        click.echo("Test ran successfully")


@cli.command("logs", help="Get logs for container. Defaults to test logs, specify STAGE argument for install or update logs.")
@click.argument("stage", default="test")
def logs(stage: str):
    dock_worker = CallDocker(global_host)
    with docker_class.open_init_file() as data:
        logs = b""
        if stage.lower() == "install":
            logs = dock_worker.get_logs(data.install_container)
        elif stage.lower() == "update":
            logs = dock_worker.get_logs(data.update_container)
        else:
            logs = dock_worker.get_logs(data.test_container)
        
        click.echo(logs.decode("utf-8"))
