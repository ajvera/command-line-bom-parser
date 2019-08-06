import unittest
import re
from bom import *

class TestBomDotCom(unittest.TestCase):

    formatVersionRxDict = {
            1: re.compile(r'(?P<MPN>[^:]*):(?P<Manufacturer>[^:]*):(?P<ReferenceDesignators>[^:]*)'),
            2: re.compile(r'(?P<Manufacturer>[^ -- ]*) -- (?P<MPN>[^:]*):(?P<ReferenceDesignators>[^:]*)'),
            3: re.compile(r'(?P<ReferenceDesignators>[^;]*);(?P<MPN>[^;]*);(?P<Manufacturer>[^;]*)'),
        }

    """Tests the parseInputFormatMethod.

    When given one of the three defined format types a MatchObject is returned.
    """
    def testParseInputFormatReturnsMatch(self):

        inputFormats = ['TSR-1002:Panasonic:A1,D2',
        'Panasonic -- TSR-1002:A', 
        'A1,B2,C8;TSR-1002;Keystone']

        matchObject = re.compile(r'\d').search('1')

        for input in inputFormats:
            match = BOM.parseInputFormat(self, input)
            self.assertIsInstance(match, type(matchObject))

    """Tests the parseInputFormatMethod.

    When given input outside the three defined format types None is returned."""
    def testParseINputFormatReturnsNone(self):
        inputFormats = ['Life the universe and everything',
        '42', 
        'Award winning fjords']

        for input in inputFormats:
            none = BOM.parseInputFormat(self, input)
            self.assertIs(none, None)

    """Tests that invalid input formats will assign a flag attribute

    When given and invalid input format boms objects will contain an
    invalidInputFormatAttribute."""
    def testInvalidInputFormat(self):
        inputFormats = ['[]',
        '//', 
        '*&']

        for input in inputFormats:
            bom = BOM(input)
            self.assertTrue(hasattr(bom, 'invalidInputFormat'))

if __name__ == '__main__':
    unittest.main()