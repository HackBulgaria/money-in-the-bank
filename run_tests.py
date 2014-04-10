import glob
import unittest
import sys
from os.path import basename


sys.path.append("tests/")

test_file_strings = glob.glob('tests/test_*.py')

module_strings = [str[0:len(str) - 3] for str in test_file_strings]

suites = [unittest.defaultTestLoader.loadTestsFromName(basename(str))
          for str in module_strings]
testSuite = unittest.TestSuite(suites)
text_runner = unittest.TextTestRunner().run(testSuite)
