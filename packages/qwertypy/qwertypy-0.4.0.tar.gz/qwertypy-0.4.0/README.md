# qwertypy

My personal utilities library.

## Installation

```bash
pip install qwertypy
```

### Upgrade

```bash
pip install --upgrade qwertypy
```

## Usage

-   Try on colab: [Click here](https://colab.research.google.com/drive/1SK96YfBgIPY-CKNfvQxvBKkJnNA7fSCe?usp=sharing)

### `qwertypy.greetings`

```py
import qwertypy.greetings as qpyGreetings

print(qpyGreetings.hello())
```

### `qwertypy.tickertape.companies`

```py
import qwertypy.tickertape.companies as ttCompanies

topCompanies = ttCompanies.getTopCompanies()
print("TOP = ", len(topCompanies))
# print("ALL = ", len(ttCompanies.getAllCompanies()))

ttName = "reliance-industries-RELI"
companyInfo = ttCompanies.getCompanyInfo(ttName)
print(companyInfo)
```

### `qwertypy.tickertape.financials`

```py
import qwertypy.tickertape.financials as ttFinancials

ttName = "reliance-industries-RELI"
for statementType in ttFinancials.statementTypes:
    statement = ttFinancials.getStatement(ttName, statementType)
    print(statementType, type(statement))
```
