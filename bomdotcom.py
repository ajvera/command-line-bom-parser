import sys
import re



def parse():
    for line in sys.stdin:
        if line.rstrip == 2:
            continue
        bom = BOM(line.rstrip())
        print(bom.mpn)
        print(bom.manufacturer)
        print(bom.referenceDesignators)
        print('\n')


class BOM:
    """ A basic class to encapsulate BOM data from a variety of formats"""

    formatVersionRxDict = {
            1: re.compile(r'([^:]*:[^:]*:[^:]*)'),
            2: re.compile(r'([^ -- ]* -- [^:]*:[^:]*)'),
            3: re.compile(r'([^;]*;[^;]*;[^;]*)'),
        }

    def parseFormatVersion(self, originalBOM):

        for key, rx in self.formatVersionRxDict.items():
            match = rx.search(originalBOM)
            if match:
                self.formatVersion = key

        return None

    def setBOMData(self, originalBOMString):
        if self.formatVersion == 1:
            bomArray = originalBOMString.split(':')
            self.mpn = bomArray[0]
            self.manufacturer = bomArray[1]
            self.referenceDesignators = bomArray[2].split(',')
        elif self.formatVersion == 2:
            bomArray = originalBOMString.split(' -- ')
            self.manufacturer = bomArray[0]
            self.mpn = bomArray[1].split(':')[0]
            self.referenceDesignators = bomArray[1].split(':')[1].split(',')
        elif self.formatVersion == 3:
            bomArray = originalBOMString.split(';')
            self.referenceDesignators = bomArray[0].split(',')
            self.mpn = bomArray[1]
            self.manufacturer = bomArray[2]

    def __init__(self, originalBOMString):
        self.originalBOMString = originalBOMString
        self.parseFormatVersion(originalBOMString)
        self.setBOMData(originalBOMString)

parse()