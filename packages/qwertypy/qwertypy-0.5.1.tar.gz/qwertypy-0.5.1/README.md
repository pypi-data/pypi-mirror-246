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

### `qwertypy.tickertape`

#### `qwertypy.tickertape.companies`

```py
import qwertypy.tickertape.companies as ttCompanies

topCompanies = ttCompanies.getTopCompanies()
print("TOP = ", len(topCompanies))
# print("ALL = ", len(ttCompanies.getAllCompanies()))

ttName = "reliance-industries-RELI"
companyInfo = ttCompanies.getCompanyInfo(ttName)
print(companyInfo)
```

#### `qwertypy.tickertape.financials`

```py
import qwertypy.tickertape.financials as ttFinancials

ttName = "reliance-industries-RELI"
for statementType in ttFinancials.statementTypes:
    statement = ttFinancials.getStatement(ttName, statementType)
    print(statementType, type(statement))

ttName = "reliance-industries-RELI"
statementType = ttFinancials.statementTypes["income"]
statement = ttFinancials.getStatement(ttName, statementType)
yearsAndValues = ttFinancials.getYearsAndValues(statement, "incDps")
print(yearsAndValues)
```

### `qwertypy.data_analysis`

#### `qwertypy.data_analysis.regression`

```py
import qwertypy.data_analysis.regression as qpyRegression

xTrain = [1, 2, 3, 4, 5, 6]
yTrain = [2, 4, 6, 8, 10, 12]
model = qpyRegression.QpyLinearRegression(xTrain, yTrain)
model.train()
yPredict = model.getPrediction()
print("yPredict: ", yPredict)

xPredict2 = [10, 11]
yExpected = [20, 22]
yPredict2 = model.getPrediction(xPredict2)
print("yPredict2: ", yPredict2)
```

### `qwertypy.data_plots`

#### `qwertypy.data_plots.trend_plot`

```py
import qwertypy.data_analysis.regression as qpyRegression
import qwertypy.data_plots.trend_plot as qpyTrendPlot
import qwertypy.tickertape.companies as ttCompanies
import qwertypy.tickertape.financials as ttFinancials

ttName = "reliance-industries-RELI"
companyInfo = ttCompanies.getCompanyInfo(ttName)
statementType = ttFinancials.statementTypes["income"]
statement = ttFinancials.getStatement(ttName, statementType)
yearsAndValues = ttFinancials.getYearsAndValues(statement, "incTrev")
xTrain = [int(x) for x in list(yearsAndValues.keys())]
yTrain = [yearsAndValues[x] for x in yearsAndValues]
model = qpyRegression.QpyLinearRegression(xTrain, yTrain)
model.train()
yPredict = [round(val, 2) for val in model.getPrediction()]
qpyTrendPlot.trendPlot(
    xTrain, yTrain,
    "Years", "Revenue (INR Cr.)", companyInfo["name"],
    trendValues = yPredict,
    legends = ["Revenue trend", "Revenue (INR Cr.)"],
    text = "text", watermark = "qwertypy",
    # saveToFile = "testImage.jpg",
    # showValues = True
)
```
