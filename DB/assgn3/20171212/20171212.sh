#!/bin/bash
if [ "$#" = 2 ]; then
	    python3 20171212_1.py "$1" "$2"
	else
		python3 20171212_2.py "$1"
fi
