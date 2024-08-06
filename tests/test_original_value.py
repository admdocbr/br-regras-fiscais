import unittest
from decimal import Decimal

from br_regras_fiscais.taxes_calc import TaxesPercents, original_nota_value


class TestOriginalValue(unittest.TestCase):
    def test_calc_ir_inferior_10_reais(self):
        # IR tax is 1.5% so the value must be lass than 666.666....
        initial_value = Decimal("666.66")
        value = original_nota_value(initial_value)
        taxes_values = value * TaxesPercents().crf_taxes
        reverted_value = taxes_values + initial_value
        rounded_result = reverted_value.quantize(Decimal("0.00"))
        assert value == rounded_result

    def test_calc_CRF_inferior_10_reais(self):
        # CRF taxes are 4.65% so the value must be lass than 215.05
        initial_value = Decimal("215.05")
        value = original_nota_value(initial_value)
        assert value == initial_value

    def test_calc_normal_rules(self):
        initial_value = Decimal("1000.00")
        value = original_nota_value(initial_value)
        taxes_values = value * TaxesPercents().all_taxes
        reverted_value = taxes_values + initial_value
        rounded_result = reverted_value.quantize(Decimal("0.00"))
        assert value == rounded_result
