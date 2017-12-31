import json


def write_to_file(opts, init_file='dock-runner-init.json'):
    """
    Writes to the init file

    :param init_file: (str)
    :param opts: (dict)
    :return:
    """
    with open(init_file, 'w') as f:
        json.dump(opts, f)


def read_file(init_file='dock-runner-init.json'):
    """
    Reads the file

    :param init_file: (str)
    :return: (dict)
    """
    with open(init_file, 'r') as f:
        ans = json.load(f)
    return ans
