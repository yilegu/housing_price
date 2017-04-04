## How predction works

Based on previous monthly prices, to predict a future price several months from now, we have two options, as illustrated below.
For this study, the prediciton is based on Option 1.

### Option 1
_Advantages_: Can be more accurate if the most recent prices are better indicators.

_Disadvantages_: To make predictions several months into the future, values predicted need to be used as independent variables (__x8__ and __x9__ here).

Here, we want to make predictions three months into the future. 

Model parameters: theta0, theta1, theta2, theta3

|Month |   Price ($1000)         |      Prediction of Price ($1000)         |
|------| ------------------------| -----------------------------------------|
|09/2016  | x1 = 100             |  N/A            |
|10/2016  | x2 = 110            |  N/A             |
|11/2016 |  x3 = 120            |  N/A             |
|12/2016  | x4 = 120            |  theta0 + x1* theta1 + x2* theta2 + x3* theta3|
|01/2017  | x5 = 110            |  theta0 + x2* theta1 + x3* theta2 + x4* theta3|
|02/2017  | x6 = 140            |  theta0 + x3* theta1 + x4* theta2 + x5* theta3|
|03/2017  | x7 = 150            |  theta0 + x4* theta1 + x5* theta2 + x6* theta3|
|04/2017  | x8 =  ?             |  theta0 + x5* theta1 + x6* theta2 + x7* theta3|
|05/2017  | x9 =  ?             |  theta0 + x6* theta1 + x7* theta2 + __x8__* theta3|
|06/2017  | x10 = ?             |  theta0 + x7* theta1 + __x8__* theta2 + __x9__* theta3|

### Option 2
_Advantages_: Predictions several months into the future can be purely based on historical data alone.

_Disadvantages_: Can be less accurate if the most recent prices are better indicators.


Here, we want to make predictions three months into the future. 

Model parameters: theta0, theta1, theta2, theta3

|Month |   Price ($1000)         |      Prediction of Price ($1000)         |
|------| ------------------------| -----------------------------------------|
|09/2016  | x1 = 100             |  N/A |
|10/2016  | x2 = 110            |  N/A  |
|11/2016 |  x3 = 120            |  N/A |
|12/2016  | x4 = 120            |  N/A |
|01/2017  | x5 = 110            |  N/A |
|02/2017  | x6 = 140            |  theta0 + x1* theta1 + x2* theta2 + x3* theta3 |
|03/2017  | x7 = 150            |  theta0 + x2* theta1 + x3* theta2 + x4* theta3|
|04/2017  | x8 =  ?             |  theta0 + x3* theta1 + x4* theta2 + x5* theta3|
|05/2017  | x9 =  ?             |  theta0 + x4* theta1 + x5* theta2 + x6* theta3|
|06/2017  | x10 = ?             |  theta0 + x5* theta1 + x6* theta2 + x7* theta3|
