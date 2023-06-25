from unittest import TestCase

from store.logic import operations


class LogicTestCase(TestCase):

    def test_plus(self):
        result = operations(6, 13, '+')
        self.assertEqual(19, result)

    def test_minus(self):
        result = operations(6, 13, '-')
        self.assertEqual(-7, result)

    def test_multiply(self):
        result = operations(6, 13, '*')
        self.assertEqual(78, result)

    def test_division(self):
        result = operations(6, 13, '/')
        self.assertEqual(6/13, result)
