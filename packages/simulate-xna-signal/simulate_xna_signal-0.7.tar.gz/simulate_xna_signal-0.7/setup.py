"""Python setup.py for project_name package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="simulate_xna_signal",
    version="0.7",
    description="pip-installable python package to simulate the expected nanopore signal produced by a given genetic sequence including unnatural bases (XNA), (J, K, P, Sc, V, X, and Z from the Artificially Expanded Genetic Information System).",
    url="https://github.com/jade-minzlaff/simulate_xna_signal",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="jade-minzlaff",
    packages=find_packages(exclude=["tests", ".github"]),
    license='MIT License',
    install_requires= ["Pandas", "NumPy", "MatPlotLib"]
)