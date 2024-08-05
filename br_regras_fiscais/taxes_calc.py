from decimal import Decimal


class TaxesCalc:
    tax_values: dict = dict(
        valor_cofins=Decimal("0.03"),
        valor_csll=Decimal("0.01"),
        valor_ir=Decimal("0.015"),
        valor_pis=Decimal("0.0065"),
    )

    def original_nota_value(self, value: Decimal) -> Decimal:
        # calculate the original value
        assumed_taxes = 0
        ir_value = self.tax_values["valor_ir"]
        if value * ir_value > 10:
            assumed_taxes += ir_value

        crf_taxes = (
            self.tax_values["valor_cofins"]
            + self.tax_values["valor_pis"]
            + self.tax_values["valor_csll"]
        )
        if value * crf_taxes > 10:
            assumed_taxes += crf_taxes

        # back calculate the original value
        original_value = value / (1 - assumed_taxes)

        return original_value.quantize(Decimal("0.00"))

    # TODO call Allephy check this rules, but first understand where we are actually using it

    # @staticmethod
    # def calc_tax(self, total_value: Decimal) -> dict:
    #     # rounding
    #     for k, v in tax_values.items():
    #         tax_values[k] = round(v, 2)
    #
    #     # transform to string
    #     tax_values = {k: str(v) for k, v in tax_values.items()}
    #
    #     return tax_values
