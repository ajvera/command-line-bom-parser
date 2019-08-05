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
    print(json.dumps(outputList, sort_keys=True, indent=4))


class BOM:
    """A basic class to capture BOM data from a variety of formats."""

    """Dictionary of RegEx patterns for idenifying input format."""
    formatVersionRxDict = {
            1: re.compile(r'(?P<MPN>[^:]*):(?P<Manufacturer>[^:]*):(?P<ReferenceDesignators>[^:]*)'),
            2: re.compile(r'(?P<Manufacturer>[^ -- ]*) -- (?P<MPN>[^:]*):(?P<ReferenceDesignators>[^:]*)'),
            3: re.compile(r'(?P<ReferenceDesignators>[^;]*);(?P<MPN>[^;]*);(?P<Manufacturer>[^;]*)'),
        }
    
    """Matches the input format with RegEx pattern and returns MatchObject."""
    def parseFormatVersion(self, originalBOMString):
        for key, rx in self.formatVersionRxDict.items():
            match = rx.search(originalBOMString)
            if match:
                return match

        return None

    """Sets class variables for BOM instance.

    Keyword arguments:
    match -- MatchObject from regex format
    """
    def setBOMData(self, match):
        self.MPN = match.group('MPN')
        self.Manufacturer = match.group('Manufacturer')
        self.ReferenceDesignators = match.group('ReferenceDesignators').split(',')
        self.NumOccurrences = 1

    """Class initializer responsible for instantiating BOM objects"""
    def __init__(self, originalBOMString):
        match = self.parseFormatVersion(originalBOMString)
        self.setBOMData(match)



parse()