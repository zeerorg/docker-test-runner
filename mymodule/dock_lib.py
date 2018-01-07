import docker
from docker.errors import DockerException

from mymodule import helper


class CallDocker(object):

    def __init__(self, host: str):
        self.client = docker.DockerClient(base_url=host)

    @staticmethod
    def check_docker(host):
        try:
            if not docker.DockerClient(base_url=host).ping():
                raise DockerException
        except (NameError, DockerException):
            return False
        return True

    def create_test_image(self, install_commands: str):
        """
        Creates a docker image and commits it. Returns the name of image and the container.
        """
        container = self.client.containers.create("ubuntu:xenial", "bash -c \"{}\"".format(install_commands))
        container.start()
        container.wait()
        image = container.commit('test-runner-{}'.format(helper.get_rand_str()))
        return image.tags[0], container.name

    def create_update_container(self, image_name, update_command):
        """
        Create an update container and image

        :param host:
        :param image_name:
        :param update_command:
        :return:
        """
        image = self.client.images.get(image_name)
        container = self.client.containers.create(image, command=update_command)
        container.start()
        container.wait()
        image = container.commit(repository=helper.get_rand_str(5))
        return image.tags[0], container.name

    def run_test_container(self, update_image, test_commands):
        """
        Run the test

        :param host:
        :param update_image:
        :param test_commands:
        :return:
        """
        container = self.client.containers.create(update_image, command=test_commands)
        container.start()
        container.wait()
        return container.name


    def del_container(self, container):
        self.client.containers.get(container).remove(v=True)


    def del_image(self, image):
        self.client.images.get(image).remove()


    def pull_image(self):
        self.client.images.pull("ubuntu:xenial")

    def get_logs(self, container):
        return self.client.containers.get(container).logs(stdout=True, stderr=True)
