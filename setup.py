"""
Python setup.py for API package
"""
import io
import os

from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """
    Read the contents of a text file safely.
    """
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as file:
        content = file.read().strip()
    return content


def read_requirements(path):
    """
    Read the dependencies as a list from the file.
    """
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="fizzbuzz-api",
    version=read("api", "VERSION"),
    description="API deployment of the classic fizzbuzz",
    url="https://github.com/jgfranco17/fizzbuzz-api/",
    license="MIT",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Joaquin Franco",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["tests", ".github"]),
    install_requires=read_requirements("requirements.txt"),
    entry_points={"console_scripts": ["fizzbuzz-api= api.__main__:main"]},
)
