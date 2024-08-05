import unittest

from br_regras_fiscais.taxes_calc import TaxesCalc


class TestTaxesDict(unittest.TestCase):
    def setUp(self):
        self.taxes_calc = TaxesCalc()
