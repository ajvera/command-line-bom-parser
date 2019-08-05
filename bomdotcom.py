import sys
import re
import json


"""This method will read the stdin stream. 

Parse will take the first line of the stdin stream and set it to a variable
which will determine the output at the end of the method.

Subsequent lines will be parsed by the BOM class on instantiation. This will
create the neccisary attribues for merge, sort, count functionality. 

Finally a collection of merged and sorted 
"""
def parse():
    lineNum = 0
    output = 0
    bomCollection = []

    for line in sys.stdin:
        foundDupe = False # For identifying BOMS with dupe MPN and Manufacturer

        if lineNum > 0:
            bom = BOM(line.rstrip())

            # No need to check for duplicates on first BOM.
            if lineNum == 1:
                bomCollection.append(bom)

                # Merge and count BOMS with the same MPN and Manufacturer. 
            else:
                for b in bomCollection:
                    if b.MPN == bom.MPN and b.Manufacturer == bom.Manufacturer:
                        b.ReferenceDesignators.extend(
                                rd for rd in bom.ReferenceDesignators 
                                if rd not in b.ReferenceDesignators)
                        b.NumOccurrences += 1
                        foundDupe = True
                        break
                    
            if not foundDupe:
                bomCollection.append(bom)
            lineNum += 1

        # Set the first line in stream as output variable.
        else:
            output = int(line.rstrip())
            lineNum += 1
    
    idx = 0
    outputList = []
    sortedCollection = sorted(bomCollection, key=lambda b: b.NumOccurrences, reverse=True)

    # Add number of records to outputList equal to 
    # output defined on first line of stream
    while idx < output:
        outputList.append(sortedCollection[idx].__dict__)
        idx += 1
    
    # Print!
    print(json.dumps(outputList, indent=4))


class BOM:
    """A basic class to capture BOM data from a variety of formats."""

    """Dictionary of RegEx patterns for idenifying input format."""
    formatVersionRxDict = {
            1: re.compile(r'([^:]*:[^:]*:[^:]*)'),
            2: re.compile(r'([^ -- ]* -- [^:]*:[^:]*)'),
            3: re.compile(r'([^;]*;[^;]*;[^;]*)'),
        }
    
    """Matches the input string with the appropriate RegEx pattern."""
    def parseFormatVersion(self, originalBOMString):
        for key, rx in self.formatVersionRxDict.items():
            match = rx.search(originalBOMString)
            if match:
                return key

        return None

    """Sets class variables for BOM data based on input string and format"""
    def setBOMData(self, originalBOMString, formatVersion):
        if formatVersion == 1:
            bomArray = originalBOMString.split(':')
            self.MPN = bomArray[0]
            self.Manufacturer = bomArray[1]
            self.ReferenceDesignators = bomArray[2].split(',')
        elif formatVersion == 2:
            bomArray = originalBOMString.split(' -- ')
            self.MPN = bomArray[1].split(':')[0]
            self.Manufacturer = bomArray[0]
            self.ReferenceDesignators = bomArray[1].split(':')[1].split(',')
        elif formatVersion == 3:
            bomArray = originalBOMString.split(';')
            self.MPN = bomArray[1]
            self.Manufacturer = bomArray[2]
            self.ReferenceDesignators = bomArray[0].split(',')
        
        self.NumOccurrences = 1

    """Class initializer responsible for instantiating BOM objects"""
    def __init__(self, originalBOMString):
        formatVersion = self.parseFormatVersion(originalBOMString)
        self.setBOMData(originalBOMString, formatVersion)



parse()