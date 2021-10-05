#!/bin/bash

# This updates the version number by accessing the most recent tagged commit.
VERSION_TAG=$(git describe --tags --abbrev=0)
echo \" $VERSION_TAG | cut -c2- \" > 'cirq-superstaq/_version.py'
