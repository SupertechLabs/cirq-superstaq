#!/usr/bin/env python3

"""
Some utilities for running shell commands and printing colorized output.
"""

import os
import subprocess

# identify the root directory of this git repository
_file_dir = os.path.dirname(os.path.realpath(__file__))
root_dir = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], cwd=_file_dir, text=True
).strip()


# container for string formatting console codes
class style:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
