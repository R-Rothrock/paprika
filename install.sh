#!/bin/bash
# https://github.com/R-Rothrock/paprika

# confirming Cython installation
python3 -m pip install cython

cython ./paprika.py

gcc *.c -o paprika

sudo cp paprika /usr/local/bin

