#!/bin/bash

# This updates the version number by accessing the most recent tagged commit.
echo "__version__ =" \"$(git describe --tags --abbrev=0 | cut -c2-)\" > 'cirq-superstaq/_version.py'
