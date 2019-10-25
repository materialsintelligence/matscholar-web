#!/bin/bash

# Run this to format the project.

isort -rc .
black .
flake8 .