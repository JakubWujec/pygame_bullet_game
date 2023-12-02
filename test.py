import unittest

loader = unittest.TestLoader()
tests = loader.discover("app")
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
