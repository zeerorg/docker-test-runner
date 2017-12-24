from setuptools import setup, find_packages

setup(
    name="Docker Task Runner",
    version='0.0.1',
    description="A tool to run tests in docker",
    author="Rishabh Gupta(zeerorg)",
    packages=find_packages(),
    install_requires=[
        'Click',
        'docker'
    ],
    entry_points="""
        [console_scripts]
        dock-runner=main:cli
    """
)
