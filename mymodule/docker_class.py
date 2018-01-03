import json
import os

from contextlib import contextmanager


@contextmanager
def open_init_file(init_file=None):
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
    def install_command(self):
        return self.dictionary.get("install").get("command")
        pass

    @install_command.setter
    def install_command(self, val):
        self.dictionary["install"] = {
            "command": val,
            "logs": ""
        }

    @property
    def update_command(self):
        return self.dictionary.get("update").get("command")

    @update_command.setter
    def update_command(self, val):
        self.dictionary["update"] = {
            "command": val,
            "logs": ""
        }

    @property
    def test_command(self):
        return self.dictionary.get("test").get("command")

    @test_command.setter
    def test_command(self, val):
        self.dictionary["test"] = {
            "command": val,
            "logs": ""
        }

    @property
    def image(self):
        return self.dictionary.get("image").get("command")

    @image.setter
    def image(self, val):
        self.dictionary["image"] = val

    @property
    def install_logs(self):
        return self.dictionary.get("install").get("logs")

    @install_logs.setter
    def install_logs(self, val):
        self.dictionary["install"]["logs"] = val

    def close(self):
        with open(self.init_file, 'w') as f:
            json.dump(self.dictionary, f, indent=4, sort_keys=True)

    def clear(self):
        self.dictionary = {}
