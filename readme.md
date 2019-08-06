# BOMDOTCOM

## Overview
Command line tool that will take arbitrary number of lines as input
from stdin. First line determines output, subsequent lines are parsed into
coherent BOM data that has been merged, sorted and counted.

### Instructions
bomdotcom has been made executable. You can run the tool by piping a files output to
the tool. Example: `cat sample.txt | ./bomdotcom`.

### Notes
Implimentation allows for collection of invalid inputs and could be easily modified to expose data on invalid inputs to the user. 

A rudimenary unit testing class has been added to test basic functionality.