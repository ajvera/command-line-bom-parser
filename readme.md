# BOMDOTCOM

## Requirements
Build command line parser that will take arbitrary number of lines as input
from stdin. First line determines output, subsequent lines are for parsing data
which will inform the data conveyed in output. 

### TODO/Initial thoughts dump
. build a class for the tool which will have an attribute of numberOfLineForOutput
as well as a class method to output themost frequently occuring BOMs along with their frequency data parsed data to the terminal. 
Tool class should also have a method for analysing a set of data and creating the appropriate collections based on uniqueness of MPN/Manufacturer
. build a class for BOMs which will have attributes of inputString, formatVersion,
manufacturer, referenceDesignators, MPNs. BOM class should also have methods for parsinginput string based on the formatVersion, as well as potentially having a static method for creating BOM collections 
