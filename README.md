# Docker Test Runner
Run tests in docker container.

How TO:
```commandline
git clone https://github.com/zeerorg/docker-test-runner.git
cd docker-test-runner
pip3 install -e .
```

Start by: 

`dock-runner`

## Goals:
--host (Optional): Specify a docker url. Will be taken from environment variable `DOCKER_HOST` if not specified.
* `init` : Takes 3 arguments.
* `init-file` : Initializes from `dock-runner-init.json` file.
* `test` : Run the test
* `clean` : Delete the previous containers.


### `init` : 
Creates the `dock-runner-init.json` file.
* install : Specify install commands for ubuntu installation. These are run first time to create a docker image. Expected: Install base dependencies. Example: `apt-get update; apt-get install git python-pip; git clone $something`. These are persisted.    
* update : Specify commands which update the test environment every time they are run. These are run to fetch the newest code changes. These may or may not be persisted. 
* test : Specify test commands which run the test. The output of these commands is logged on terminal.

#### `dock-runner-init.json` file:

* image : Specifies the image name
* install/update/test : Specifies the install/update/test command respectively. Also contains the logs for inspection.
* containers (list) : Contains list of containers run. TODO: also store logs.
* host : The host url (If specified)


#### Extra functionality: 
* Determine if the test has completed.
* trigger post completion command
* 

### Example usage : (TODO)


