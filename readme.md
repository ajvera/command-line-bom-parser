# BOMDOTCOM

## Overview
Command line tool that will take arbitrary number of lines as input
from stdin. First line determines output, subsequent lines are parsed into
coherent BOM data with that has been merged, sorted and counted.

### TODO/Initial thoughts dump
bomdotcom has been made executable. You can run the tool by piping a files output to
the tool. Example: `cat sample.txt | ./bomdotcom`.
