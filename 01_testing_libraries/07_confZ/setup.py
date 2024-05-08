#!/usr/bin/env python
import os
from typing import List

from setuptools import find_packages, setup

# Package name used to install via pip (shown in `pip freeze` or `conda list`)
MODULE_NAME = "tchonfz"

# How this module is imported in Python (name of the folder inside `src`)
MODULE_NAME_IMPORT = "tchonfz"

# Repository name
REPO_NAME = "tchonfz"

# File to get direct dependencies from (used by pip)
REQUIREMENTS_FILE = "requirements.in"


def get_version() -> str:
    with open(os.path.join("src", MODULE_NAME_IMPORT, "resources", "VERSION")) as f:
        return f.read().strip()


def requirements_from_pip(filename: str) -> List[str]:
    with open(filename, "r") as pip:
        return [
            line.strip() for line in pip if not line.startswith("#") and line.strip()
        ]


SETUP_ARGS = {
    "name": MODULE_NAME,
    "url": "https://github.com/nubank/{:s}".format(REPO_NAME),
    "author": "Rafael S. Calsaverini",
    "package_dir": {"": "src"},
    "packages": find_packages("src"),
    "version": get_version(),
    "python_requires": ">=3.6,<3.10",
    "install_requires": requirements_from_pip(REQUIREMENTS_FILE),
    "extras_require": {"test_deps": requirements_from_pip("requirements_test.txt")},
    "include_package_data": True,
    "zip_safe": False,
}

if __name__ == "__main__":
    setup(**SETUP_ARGS)
