# -*- coding: utf-8 -*-

import unittest
import logging


class TestRunner(object):
    def __init__(self):
        self.unittest_runner = unittest.TextTestRunner()
        self.test_suite = unittest.TestSuite()

    def add_test(self, test):
        if not isinstance(test, unittest.TestCase):
            logging.error('{} ({}) is not type of {}'\
                          .format(test, type(test), unittest.TestCase))
            return

        self.test_suite.addTest(test)

    def add_tests(self, tests_list):
        if not isinstance(tests_list, list):
            logging.error('{} ({}) is not type of {}'\
                          .format(tests_list, type(tests_list), list))
            return
        for test in tests_list:
            self.test_suite.addTest(test)

    def run_tests(self):
        for testcase in self.test_suite:
            self.unittest_runner.run(testcase)