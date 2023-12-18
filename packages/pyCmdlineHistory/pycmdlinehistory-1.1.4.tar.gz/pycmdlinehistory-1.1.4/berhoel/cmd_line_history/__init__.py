#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Save command line history and provide a command line completer for python.
"""

from __future__ import division, print_function, absolute_import, unicode_literals

# Standard library imports.
from atexit import register
from readline import set_pre_input_hook

# Third party library imports.
import __main__

# Local library imports.
from .history import History

__date__ = "2023/12/17 18:06:23 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = "Copyright © 2006 by Sunjoong LEE"
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


try:
    # Local library imports.
    from ._version import __version__
except ImportError:
    __version__ = "0.0.0.invalid0"


def save_history(history_path=None):
    # Standard library imports.
    from readline import write_history_file

    # Local library imports.
    from .history import HISTORY_PATH

    if history_path is None:
        history_path = HISTORY_PATH
    write_history_file(history_path)


register(save_history)


def hook():
    # Standard library imports.
    from readline import set_pre_input_hook

    # Third party library imports.
    import __main__

    set_pre_input_hook()
    delattr(__main__, "History")
    delattr(__main__, "__file__")


set_pre_input_hook(hook)
setattr(__main__.__builtins__, "history", History())

# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
