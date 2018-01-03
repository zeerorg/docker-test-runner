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
    client = _get_client(host)
    image = client.images.get(image_name)
    container = client.containers.create(image, command=update_command)
    container.start()
    container.wait()
    image = container.commit(repository=helper.get_rand_str(5))
    return image.tags[0], container.name


def run_test_container(host, update_image, test_commands):
    pass


def pull_image(host):
    client = _get_client(host)
    client.images.pull("ubuntu:xenial")
    pass
