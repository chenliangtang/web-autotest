# -*- coding: utf-8 -*-

import os
import unittest
import logging
from importlib import import_module


class TestRunner(object):
    def __init__(self):
        self.unittest_runner = unittest.TextTestRunner()
        self.test_suite = unittest.TestSuite()
        self.test_results = []
        self.test_loader = unittest.TestLoader()
        self.load_testcases = []

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
        self.test_suite.addTests(tests_list)

    def load_test(self, testcase):
        return self.test_loader.loadTestsFromTestCase(testcase)

    def load_tests(self, testcases):
        for testcase in testcases:
            self.load_testcases.append(self.load_test(testcase))

    def run_tests(self):
        for testcase in self.test_suite:
            result = self.unittest_runner.run(testcase)
            self.test_results.append((testcase, result))


def make_import_files(module_path):
    import_files_path = []
    for _, _, files in os.walk(module_path):
        for file in files:
            if file.endswith('.py'):
                file = file.strip('.py')
                import_files_path.append(module_path + '.' + file)
    return import_files_path


def make_testcases_with_test_function(import_files_path):
    testcases = []
    for file_path in import_files_path:
        modules = import_module(file_path)
        for module_name, module_value in vars(modules).items():
            if isinstance(module_value, type):
                for attribute in dir(module_value):
                    if attribute.startswith('test_'):
                        testcase = module_value(attribute)
                        testcases.append(testcase)
    return testcases


def make_testcases(import_files_path):
    testcases = []
    for file_path in import_files_path:
        modules = import_module(file_path)
        for module_name, module_value in vars(modules).items():
            if isinstance(module_value, type):
                testcase = module_value
                testcases.append(testcase)
    return testcases


def make_unittest_testcases():
    module_path = 'testsuites'
    import_files_path = make_import_files(module_path)
    return make_testcases(import_files_path)