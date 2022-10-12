from setuptools import setup

setup(
    name="filestore",
    version="0.1",
    packages=[""],
    url="",
    license="MIT",
    author="vavuthu",
    author_email="vavuthu@redhat.com",
    description=(
        "file store service that stores plain-text "
        "files (HTTP server and a command line client)"
    ),
    install_requires=[
        "bs4",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "store=client.main:main",
            "run-server=server.server:run_server",
        ],
    },
)
