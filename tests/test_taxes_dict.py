import unittest
from decimal import Decimal

from br_regras_fiscais.taxes_calc import TaxesCalc


class TestTaxesDict(unittest.TestCase):
    def setUp(self):
        self.taxes_calc = TaxesCalc()

    def test_calc_ir_inferior_10_reais(self):
        # IR tax is 1.5% so the value must be lass than 666.666....
        initial_value = Decimal("666.66")
        taxes = self.taxes_calc.tax_dict(initial_value)
        assert "valor_ir" in taxes.keys()
        assert taxes["valor_ir"] == 0

    def test_calc_CRF_inferior_10_reais(self):
        # CRF taxes are 4.65% so the value must be lass than 215.05
        initial_value = Decimal("215.05")
        taxes = self.taxes_calc.tax_dict(initial_value)
        for key in self.taxes_calc.CRF_taxes_keys:
            assert key in taxes
            assert taxes[key] == 0

    def test_calc_normal_rules(self):
        initial_value = Decimal("1000.00")
        taxes = self.taxes_calc.tax_dict(initial_value)
        print(taxes)
        assert taxes["valor_cofins"] == 30
        assert taxes["valor_csll"] == 10
        assert taxes["valor_ir"] == 15
        assert taxes["valor_pis"] == 6.5
