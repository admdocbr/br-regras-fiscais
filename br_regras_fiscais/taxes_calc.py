from decimal import Decimal
from dataclasses import dataclass


@dataclass
class TaxesValues:
    cofins: Decimal
    csll: Decimal
    ir: Decimal
    pis: Decimal

    @property
    def sum_crf(self) -> Decimal:
        return self.pis + self.csll + self.cofins


@dataclass
class TaxesPercents:
    cofins = Decimal("0.03")
    csll = Decimal("0.01")
    ir = Decimal("0.015")
    pis = Decimal("0.0065")

    @property
    def crf_taxes(self) -> Decimal:
        # Calculate the sum of the crf taxes percents
        return self.pis + self.csll + self.cofins

    @property
    def all_taxes(self) -> Decimal:
        # Calculate the sum of all taxes percents
        return self.crf_taxes + self.ir


def original_nota_value(value: Decimal) -> Decimal:
    """
    :param value: The payment received after taxes
    :return: Outputs the original value from the Nota Fiscal (total_value)
    """
    # calculate the original value
    assumed_taxes = 0
    taxes_percents = TaxesPercents()
    ir_value = taxes_percents.ir * value
    if ir_value > 10:
        assumed_taxes += taxes_percents.ir

    crf_taxes = value * taxes_percents.crf_taxes

    if crf_taxes > 10:
        assumed_taxes += taxes_percents.crf_taxes

    # back calculate the original value
    original_value = value / (1 - assumed_taxes)

    return original_value.quantize(Decimal("0.00"))


def tax_dict(total_value: Decimal) -> TaxesValues:
    """
    :param total_value: Total value of the Nota Fiscal
    :return: A Taxes DataClass with the values for Imposto de Renda (IR), COFINS, CSLL, PIS
    """
    taxes_percents = TaxesPercents()

    tax_values = TaxesValues(
        cofins=total_value * taxes_percents.cofins,
        csll=total_value * taxes_percents.csll,
        ir=total_value * taxes_percents.ir,
        pis=total_value * taxes_percents.pis,
    )
    if tax_values.ir < 10:
        tax_values.ir = 0

    if tax_values.sum_crf < 10:
        tax_values.pis = 0
        tax_values.csll = 0
        tax_values.cofins = 0
    return tax_values
