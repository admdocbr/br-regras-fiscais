# br-regras-fiscais

## A lib to calculate taxes on Brasil for NFe, and also get total NFe value from a payment. 

It takes in account if *Imposto de Renda* is less than R$ 10,00, and same for *CRF* (PIS, COFINS,CSLL)

---
### original_nota_value
Using the paid valued from a Transaction it returns the original total value of a NF

---
### tax_dict
Returns a Data Class with the taxes values:

    @dataclass
    class TaxesValues:
        cofins: Decimal
        csll: Decimal
        ir: Decimal
        pis: Decimal

        @property
        def sum_crf(self) -> Decimal:
            return self.pis + self.csll + self.cofins

