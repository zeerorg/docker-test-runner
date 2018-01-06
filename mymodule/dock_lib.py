import docker
from docker.errors import DockerException

from mymodule import helper


def _get_client(host):
    return docker.DockerClient(base_url=host)


def check_docker(host):
    """
    Checks if docker is running.

    :param host: (str)
    :return: (bool)
    """
    try:
        if not _get_client(host).ping():
            raise DockerException
    except (NameError, DockerException):
        return False
    return True


def create_image(host, install_commands):
    """
    Creates a docker image and commits it. Returns the name of image and the container.

    :param host: (str)
    :param install_commands: (str)
    :return: (str)
    """
    client = _get_client(host)
    container = client.containers.create("ubuntu:xenial", "bash -c \"{}\"".format(install_commands))
    container.start()
    container.wait()
    image = container.commit('test-runner-{}'.format(helper.get_rand_str()))
    return image.tags[0], container.name


def is_image_avail(host, image):
    pass


def create_update_container(host, image_name, update_command):
    """
    Create an update container and image

    :param host:
    :param image_name:
    :param update_command:
    :return:
    """
    client = _get_client(host)
    image = client.images.get(image_name)
    container = client.containers.create(image, command=update_command)
    container.start()
    container.wait()
    image = container.commit(repository=helper.get_rand_str(5))
    return image.tags[0], container.name


def run_test_container(host, update_image, test_commands):
    """
    Run the test

    :param host:
    :param update_image:
    :param test_commands:
    :return:
    """
    client = _get_client(host)
    container = client.containers.create(update_image, command=test_commands)
    container.start()
    container.wait()
    return container.name
    pass


def del_container(host, container):
    client = _get_client(host)
    client.containers.get(container).remove(v=True)


def del_image(host, image):
    client = _get_client(host)
    client.images.get(image).remove()


def pull_image(host):
    client = _get_client(host)
    client.images.pull("ubuntu:xenial")
    pass
