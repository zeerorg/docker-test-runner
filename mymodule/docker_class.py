import json
import os

from contextlib import contextmanager


@contextmanager
def open_init_file(init_file: str = None):
    """
    Context manager for opening init file and saving when it closes

    :param init_file:
    :return:
    """
    docker_file = _DockerClass()
    if init_file:
        docker_file = _DockerClass(init_file)
    yield docker_file
    docker_file.close()


class _DockerClass:
    """
    Class to communicate with the init file
    """

    def __init__(self, init_file='dock-runner-init.json'):

        self.dictionary = {}

        if os.path.isfile(init_file):
            with open(init_file, 'r') as f:
                s = f.read()
            if s:
                self.dictionary = json.loads(s)

        self.init_file = init_file

    @property
    def install_command(self) -> str:
        return self.dictionary.get("install").get("command")

    @install_command.setter
    def install_command(self, val: str) -> None:
        self.dictionary["install"] = {
            "command": val,
            "container": ""
        }

    @property
    def update_command(self) -> str:
        return self.dictionary.get("update").get("command")

    @update_command.setter
    def update_command(self, val):
        self.dictionary["update"] = {
            "command": val,
            "container": ""
        }

    @property
    def test_command(self):
        return self.dictionary.get("test").get("command")

    @test_command.setter
    def test_command(self, val):
        self.dictionary["test"] = {
            "command": val,
            "container": ""
        }

    @property
    def image(self):
        return self.dictionary.get("image")

    @image.setter
    def image(self, val):
        self.dictionary["image"] = val

    @property
    def install_container(self):
        return self.dictionary.get("install").get("container")

    @install_container.setter
    def install_container(self, val):
        self.dictionary["install"]["container"] = val

    @property
    def update_container(self):
        return self.dictionary.get("update").get("container")

    @update_container.setter
    def update_container(self, val):
        self.dictionary["update"]["container"] = val

    @property
    def test_container(self):
        return self.dictionary.get("test").get("container")

    @test_container.setter
    def test_container(self, val):
        self.dictionary["test"]["container"] = val

    @property
    def update_image(self):
        return self.dictionary.get("update").get("image")

    @update_image.setter
    def update_image(self, val):
        self.dictionary["update"]["image"] = val

    def close(self):
        with open(self.init_file, 'w') as f:
            json.dump(self.dictionary, f, indent=4, sort_keys=True)

    def clear(self):
        self.dictionary = {}
