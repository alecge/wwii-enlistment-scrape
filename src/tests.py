import unittest
import scraper


class TestScraperMethods(unittest.TestCase):
    def test_generate_field_params(self):
        self.assertEqual(scraper.generate_field_params(1), '')