#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `cmd_line_history`.
"""
from __future__ import division, print_function, absolute_import, unicode_literals

# Third party library imports.
import toml
import pytest

# First party library imports.
from berhoel import cmd_line_history

try:
    # Standard library imports.
    from pathlib import Path
except:
    # Third party library imports.
    from pathlib2 import Path

__date__ = "2022/08/09 21:30:03 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


@pytest.fixture
def base_path():
    base_path = Path(__file__).parent
    while not (base_path / "pyproject.toml").is_file():
        base_path = base_path.parent
    return base_path


@pytest.fixture
def config(base_path):
    return base_path / "pyproject.toml"


@pytest.fixture
def toml_data(config):
    return toml.load(config.open("r"))


def test_version(toml_data):
    """Testing for consistent version number."""
    assert cmd_line_history.__version__ == toml_data["tool"]["poetry"]["version"]


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
