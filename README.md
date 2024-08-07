# br-regras-fiscais

## A lib to calculate taxes on Brasil for NFe, and also get total NFe value from a payment. 

It takes in account if *Imposto de Renda* is less than R$ 10,00, and same for *CRF* (PIS, COFINS,CSLL)

# Installation

br-regras-fiscais can be installed via pypi.

```
pip install br-regras-fiscais
```

---
# Usage

### original_nota_value
Using the paid valued from a Transaction it returns the original total value of a NF

```
>>> from br_regras_fiscais.taxes_calc import original_nota_value
>>> original_nota_value(1000)
Decimal('1065.53')
```

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

```
>>> from br_regras_fiscais.taxes_calc import tax_dict
>>> tax_dict(1000)
TaxesValues(cofins=Decimal('30.00'), csll=Decimal('10.00'), ir=Decimal('15.000'), pis=Decimal('6.5000'))
```