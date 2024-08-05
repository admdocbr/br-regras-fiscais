from decimal import Decimal


class TaxesCalc:
    CRF_taxes_keys = ["valor_cofins", "valor_pis", "valor_csll"]

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

        # crf_taxes = sum(x for )
        if value * crf_taxes > 10:
            assumed_taxes += crf_taxes

        # back calculate the original value
        original_value = value / (1 - assumed_taxes)

        return original_value.quantize(Decimal("0.00"))

    # TODO call Allephy check this rules, but first understand where we are actually using it
    # TODO output dict for nfe on core_api
    def calc_tax(self, total_value: Decimal) -> dict:
        tax_values = dict(
            valor_cofins=total_value * self.tax_values["valor_cofins"],
            valor_csll=total_value * self.tax_values["valor_csll"],
            valor_ir=total_value * self.tax_values["valor_ir"],
            valor_pis=total_value * self.tax_values["valor_pis"],
        )
        if tax_values["valor_ir"] < 10:
            tax_values["valor_ir"] = 0

        crf_value = sum(tax_values[key] for key in self.CRF_taxes_keys)
        if crf_value < 10:
            tax_values["valor_pis"] = 0
            tax_values["valor_csll"] = 0
            tax_values["valor_cofins"] = 0
        return tax_values
