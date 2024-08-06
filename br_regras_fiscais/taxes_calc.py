from decimal import Decimal
from dataclasses import dataclass


@dataclass
class Taxes:
    cofins: Decimal
    csll: Decimal
    ir: Decimal
    pis: Decimal


CRF_taxes_keys = ["cofins", "pis", "csll"]


@dataclass
class TaxesPercents:
    cofins = Decimal("0.03")
    csll = Decimal("0.01")
    ir = Decimal("0.015")
    pis = Decimal("0.0065")

    @property
    def crf_taxes(self) -> Decimal:
        # Correctly calculate the sum of the crf taxes percents
        return self.pis + self.cofins + self.pis

    @property
    def all_taxes(self) -> Decimal:
        # Correctly calculate the sum of all taxes percents
        return self.crf_taxes + self.ir


class TaxesCalc:
    def original_nota_value(self, value: Decimal) -> Decimal:
        """
        :param value: The payment received after taxes
        :return: Outputs the original value from the Nota Fiscal (total_value)
        """
        # calculate the original value
        assumed_taxes = 0
        ir_value = TaxesPercents().ir * value
        if ir_value > 10:
            assumed_taxes += TaxesPercents().ir

        crf_taxes = value * TaxesPercents().crf_taxes

        if crf_taxes > 10:
            assumed_taxes += TaxesPercents().crf_taxes

        # back calculate the original value
        original_value = value / (1 - assumed_taxes)

        return original_value.quantize(Decimal("0.00"))

    def tax_dict(self, total_value: Decimal) -> Taxes:
        """
        :param total_value: Total value of the Nota Fiscal
        :return: A Taxes DataClass with the values for Imposto de Renda (IR), COFINS, CSLL, PIS
        """

        tax_values = Taxes(
            cofins=total_value * TaxesPercents.cofins,
            csll=total_value * TaxesPercents.csll,
            ir=total_value * TaxesPercents.ir,
            pis=total_value * TaxesPercents.pis,
        )
        if tax_values.ir < 10:
            tax_values.ir = 0

        crf_value = sum(tax_values.__dict__[key] for key in CRF_taxes_keys)
        if crf_value < 10:
            tax_values.pis = 0
            tax_values.csll = 0
            tax_values.cofins = 0
        return tax_values
