import re

class BOM:
    """A basic class to capture BOM data from a variety of input formats."""

    """Dictionary of RegEx patterns for idenifying input format."""
    formatVersionRxDict = {
            1: re.compile(r'(?P<MPN>[^:]*):(?P<Manufacturer>[^:]*):(?P<ReferenceDesignators>[^:]*)'),
            2: re.compile(r'(?P<Manufacturer>[^ -- ]*) -- (?P<MPN>[^:]*):(?P<ReferenceDesignators>[^:]*)'),
            3: re.compile(r'(?P<ReferenceDesignators>[^;]*);(?P<MPN>[^;]*);(?P<Manufacturer>[^;]*)'),
        }
    
    """Matches the input format with RegEx pattern and returns MatchObject."""
    def parseInputFormat(self, originalBOMString):
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
        if match == None:
            self.invalidInputFormat = True
            return 

        self.MPN = match.group('MPN')
        self.Manufacturer = match.group('Manufacturer')
        self.ReferenceDesignators = match.group('ReferenceDesignators').split(',')
        self.NumOccurrences = 1

    """Class initializer responsible for instantiating BOM objects"""
    def __init__(self, originalBOMString):
        match = self.parseInputFormat(originalBOMString)
        self.setBOMData(match)