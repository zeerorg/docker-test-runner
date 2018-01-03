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
    Creates a docker image and commits it. Returns the name of image.

    :param host: (str)
    :param install_commands: (str)
    :return: (str)
    """
    client = _get_client(host)
    container = client.containers.create("ubuntu:xenial", "bash -c \"{}\"".format(install_commands))
    container.start()
    logs = [x.decode("utf-8") for x in container.logs(stdout=True, stderr=True, stream=True)]
    logs = '\n'.join(logs)
    image = container.commit('test-runner-{}'.format(helper.get_rand_str()))
    container.remove()
    return image, logs


def is_image_avail(host, image):
    pass


def pull_image(host):
    client = _get_client(host)
    client.images.pull("ubuntu:xenial")
    pass
