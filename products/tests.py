from django.test import TestCase
from .models import Product

# Create your tests here.
"""You should always test your models, so we're just going to a very quick example of a test here.
    Try and think of what other aspects of your model you might be able to test and try them out for yourself.
    So we're creating our ProductTests, which we'll inherit from TestCase.
"""
class ProductTests(TestCase):
    """
    Here we'll define the tests that we'll run against our
    Product model
    """
    # It's important to note that if our methods don't begin with test underscore then Django won't find them

    def test_str(self):
        test_name = Product(name = 'A product')
        self.assertEqual(str(test_name), 'A product')