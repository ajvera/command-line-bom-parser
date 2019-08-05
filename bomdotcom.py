import sys
import re
import json

def parse():
    i = 0
    bomCollection = []
    output = 0
    for line in sys.stdin:
        foundDupe = False
        if i > 0:
            bom = BOM(line.rstrip())
            if i == 1:
                bomCollection.append(bom)
            else:
                for b in bomCollection:
                    if b.MPN == bom.MPN and b.Manufacturer == bom.Manufacturer:
                        b.ReferenceDesignators.extend(rd for rd in bom.ReferenceDesignators if rd not in b.ReferenceDesignators)
                        b.NumOccurrences += 1
                        foundDupe = True
                        break
                    
            if not foundDupe:
                bomCollection.append(bom)
            i += 1

        else:
            output = int(line.rstrip())
            i += 1
    
    bomCollection = sorted(bomCollection, key=lambda b: b.NumOccurrences, reverse=True)
    
    print('Begin BOM data output\n')
    
    idx = 0
    final = []
    while idx < output:
        final.append(bomCollection[idx].__dict__)
        idx += 1
    
    print(json.dumps(final, indent=4))

class BOM:
    """ A basic class to capture BOM data from a variety of formats"""

    formatVersionRxDict = {
            1: re.compile(r'([^:]*:[^:]*:[^:]*)'),
            2: re.compile(r'([^ -- ]* -- [^:]*:[^:]*)'),
            3: re.compile(r'([^;]*;[^;]*;[^;]*)'),
        }

    def parseFormatVersion(self, originalBOM):
        for key, rx in self.formatVersionRxDict.items():
            match = rx.search(originalBOM)
            if match:
                return key

        return None

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

    def __init__(self, originalBOMString):
        formatVersion = self.parseFormatVersion(originalBOMString)
        self.setBOMData(originalBOMString, formatVersion)

parse()