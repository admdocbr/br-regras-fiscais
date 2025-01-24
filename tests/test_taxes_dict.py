import unittest
from decimal import Decimal

from br_regras_fiscais.taxes_calc import tax_dict


class TestTaxesDict(unittest.TestCase):
    def test_calc_ir_inferior_10_reais(self):
        # IR tax is 1.5% so the value must be lass than 666.33....
        initial_value = Decimal("666.33")
        taxes = tax_dict(initial_value)
        assert taxes.ir == 0

    def test_calc_CRF_inferior_10_reais(self):
        # CRF taxes are 4.65% so the value must be lass than 214.84
        initial_value = Decimal("214.83")
        taxes = tax_dict(initial_value)
        assert taxes.pis == 0
        assert taxes.cofins == 0
        assert taxes.csll == 0

    def test_calc_normal_rules(self):
        initial_value = Decimal("1000.00")
        taxes = tax_dict(initial_value)
        assert taxes.cofins == 30
        assert taxes.csll == 10
        assert taxes.ir == 15
        assert taxes.pis == 6.5
