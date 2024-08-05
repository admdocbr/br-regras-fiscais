from decimal import Decimal


class TaxesCalc:
    # TODO data class python  ?

    CRF_taxes_keys = ["valor_cofins", "valor_pis", "valor_csll"]

    taxes_percents: dict = dict(
        valor_cofins=Decimal("0.03"),
        valor_csll=Decimal("0.01"),
        valor_ir=Decimal("0.015"),
        valor_pis=Decimal("0.0065"),
    )

    def original_nota_value(self, value: Decimal) -> Decimal:
        """
        :param value: The payment received after taxes
        :return: Outputs the original value from the Nota Fiscal (total_value)
        """
        # calculate the original value
        assumed_taxes = 0
        ir_value = self.taxes_percents["valor_ir"]
        if value * ir_value > 10:
            assumed_taxes += ir_value

        crf_taxes = (
            self.taxes_percents["valor_cofins"]
            + self.taxes_percents["valor_pis"]
            + self.taxes_percents["valor_csll"]
        )

        # crf_taxes = sum(x for )
        if value * crf_taxes > 10:
            assumed_taxes += crf_taxes

        # back calculate the original value
        original_value = value / (1 - assumed_taxes)

        return original_value.quantize(Decimal("0.00"))

    # TODO call Allephy check this rules, but first understand where we are actually using it
    # TODO output dict for nfe on core_api
    def tax_dict(self, total_value: Decimal) -> dict:
        """
        :param total_value: Total value of the Nota Fiscal
        :return: A dict with the values for Imposto de Renda (IR), COFINS, CSLL, PIS
        """
        tax_values = dict(
            valor_cofins=total_value * self.taxes_percents["valor_cofins"],
            valor_csll=total_value * self.taxes_percents["valor_csll"],
            valor_ir=total_value * self.taxes_percents["valor_ir"],
            valor_pis=total_value * self.taxes_percents["valor_pis"],
        )
        if tax_values["valor_ir"] < 10:
            tax_values["valor_ir"] = 0

        crf_value = sum(tax_values[key] for key in self.CRF_taxes_keys)
        if crf_value < 10:
            tax_values["valor_pis"] = 0
            tax_values["valor_csll"] = 0
            tax_values["valor_cofins"] = 0
        return tax_values
