#!/usr/bin/env python3

"""
Runs black to standardize python file formats.

Usage:
    check/format.py [--flags] -- [files]

All arguments are passed to black, along with the following default flags:
  --color : colorized output
  --line-length=100 : enforce a maximum line length of 100
  --diff : print a diff of what black would change, without changing files
  --check : signal success or failure in the return code (success = no changes to make)

The flag "--apply" is interpreted as turning off "--diff --check", causing black to apply changes.

The separator "--" can be used to run black on specific files (or directories).  If the separator
"--" does not appear in the list of arguments, this script runs black on the entire repository.
"""

import os
import subprocess
import sys

from utils import root_dir

args = ["--color", "--line-length=100", "--diff", "--check"] + sys.argv[1:]
if "--apply" in args:
    args.remove("--apply")
    args.remove("--diff")
    args.remove("--check")

if "--" not in args:
    args += ["check", "dev_tools", "docs", "examples", "cirq_superstaq", "setup.py"]

returncode = subprocess.call(["black", *args], cwd=root_dir)

if returncode == 1:
    # some files should be reformatted, but there don't seem to be any bona fide errors
    this_file = os.path.relpath(__file__)
    print(f"Run '{this_file} --apply' to format the files.")

exit(returncode)
