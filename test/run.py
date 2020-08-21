#!/usr/bin/env python3

import os
import sys
from unittest import TestLoader, TextTestRunner, TestSuite
from readalongs.log import LOGGER

# Unit tests
from test_indices import TestIndices
from test_audio import TestAudio

## End-to-End
from test_force_align import TestForceAlignment, TestXHTML


## Other tests
from test_tokenize_xml import TestTokenizer
from test_temp_file import TestTempFile
from test_prepare_cli import TestPrepareCli
from test_align_cli import TestAlignCli


loader = TestLoader()

e2e_tests = [
    loader.loadTestsFromTestCase(test) for test in (TestForceAlignment, TestXHTML)
]

indices_tests = [loader.loadTestsFromTestCase(test) for test in [TestIndices]]

other_tests = [
    loader.loadTestsFromTestCase(test)
    for test in [TestTokenizer, TestTempFile, TestPrepareCli, TestAudio, TestAlignCli]
]


def run_tests(suite):
    if suite == "e2e":
        suite = TestSuite(e2e_tests)
    elif suite == "dev":
        suite = TestSuite(indices_tests + other_tests + e2e_tests)
    elif suite == "prod" or suite == "all":
        suite = loader.discover(os.path.dirname(__file__))
    elif suite == "other":
        suite = TestSuite(other_tests)
    else:
        LOGGER.error(
            "Sorry, you need to select a Test Suite to run, like 'dev' or 'prod'"
        )

    runner = TextTestRunner(verbosity=3)
    return runner.run(suite)


if __name__ == "__main__":
    try:
        result = run_tests(sys.argv[1])
        if not result.wasSuccessful():
            raise Exception("Some tests failed. Please see log above.")
    except IndexError:
        print("Please specify a test suite to run: i.e. 'dev' or 'all'")
