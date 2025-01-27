"""

Summary => will run all tests.

Description => will run all unit tests, made for every class.

Author => Matthew Howard (mah60).
Version => 0.1 - 18/03/2018 - created basic version of test suite.
           1.0 - 04/03/2018 - This is the Final version of the code.
"""
import unittest

from test_plotter_controller import TestPlotterController as TPlot
from test_image_processor import TestImageProccesor as IPro


def run_tests():
    """
    Summary => creates a test suite.

    Description => creates a test suite that will test all unit
            tests.

            Used :
    https://www.blog.pythonlibrary.org/2016/07/07/
    python-3-testing-an-intro-to-unittest/
                    for basic tutorial on how to create unit tests in python.
    args => None

    return => None
    """
    print('--------------------------------------------------------------')
    print('starting tests')
    print('--------------------------------------------------------------')
    # create a test suite and result, to place the results in
    suite = unittest.TestSuite()
    result = unittest.TestResult()
    # -------------------------------------------------------------------
    # add to test TestSuite
    # -------------------------------------------------------------------
    suite.addTest(unittest.makeSuite(TPlot))
    suite.addTest(unittest.makeSuite(IPro))
    # -------------------------------------------------------------------
    # run TestSuite
    runner = unittest.TextTestRunner()
    print(runner.run(suite))


if __name__ == '__main__':
    run_tests()
