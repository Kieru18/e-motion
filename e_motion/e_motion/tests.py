from django.test import TestCase


class BasicTest(TestCase):
    def test_hello_world(self):
        """Basic test description"""
        x = 1
        self.assertEqual(x, 1)

    def test_not_equal(self):
        """Basic test description"""
        x = 0
        self.assertNotEqual(x, 0)
