# -*- coding: utf-8 -*-

from testcases.test_login import TestLoginPage
from testcases.test_switch_subsystem import TestSwitchSubsystem
from pageobject.driver import Browser
import testrunner

if __name__ == '__main__':
    tests = []
    test_runner = testrunner.TestRunner()
    tests.append(TestLoginPage('test_login'))
    tests.append(TestSwitchSubsystem('test_switch_subsystem'))

    test_runner.add_tests(tests)
    test_runner.run_tests()

    Browser().close_driver()


    """
    module = import_module('testcases.test_login')
    dir(module)
    for k, v in vars(module).items():
        print(k, ': ', v)
        if k == 'TestLoginPage':
            print(k, ': ', v)
            tests.append(v('test_login'))
    test_runner.add_tests(tests)
    test_runner.run_tests()
    """

