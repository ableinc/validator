import setuptools
from lib.version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="validator",
    version=__version__,
    license="GNU General Public License v3.0",
    author="AbleInc - Jaylen Douglas",
    author_email="douglas.jaylen@gmail.com",
    description="This is a request handler validation tool for RESTful API endpoints.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ableinc/validator",
    keywords=["validation tool", "validation", "api", "restful", "endpoints", "ableinc"],
    packages=["lib"],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ]
)
