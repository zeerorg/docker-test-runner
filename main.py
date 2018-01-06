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


@cli.command("init-file")
def init_file():
    host = global_host
    with docker_class.open_init_file() as data:
        click.echo("Pulling ubuntu:xenial Image ...")
        dock_lib.pull_image(host)
        click.echo("Creating test machine image. Installing packages, setting up environment. May take time ...")
        image_tag, install_logs = dock_lib.create_image(host, data.install_command)
        data.image = image_tag
        data.install_container = install_logs

    click.echo("Image created : {}".format(image_tag))


@cli.command("test")
def test() -> None:
    """
    Steps to run test container
    1. Delete update container, update image and test container
    2. Create update container from install image
    3. Create update image from update container
    4. Use update image to create test container

    """
    host = global_host
    with docker_class.open_init_file() as data:
        if data.update_container:
            dock_lib.del_container(host, data.update_container)
        if data.test_container:
            dock_lib.del_container(host, data.test_container)
        if data.update_image:
            dock_lib.del_image(host, data.update_container)

        click.echo("Creating container from image {}".format(data.image))
        data.update_image, data.update_container = dock_lib.create_update_container(host, data.image, data.update_command)
        # use image tag to create test container, container_name to write to json file
        click.echo("Running test")
        data.test_container = dock_lib.run_test_container(host, data.update_image, data.test_command)
        click.echo("Test ran successfully")
        pass
    pass
