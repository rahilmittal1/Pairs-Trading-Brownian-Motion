# Optimal Pairs Trading Strategy Using Brownian Motion





STEPS:

Get an API which gets us all the historical data of US stocks that make up the S&P500 -> API needs to be immediate. 20 years of data. Yahoo finance
Calculate correlation 0.7 above and calculate cointegration using ADF test. Select pairs of stocks
Model both stock prices using the Geometric Brownian Motion equation. Compare both stock prices to each other. Each stock will have a drift and volatility
Determine the entry and exit point thresholds based on the price ratio of the two stocks. Use Hamilton Jacobi Bellman method to optimize these entry and exit prices and regime switching
The Hamilton-Jacobi-Bellman (HJB) equations are crucial to finding the optimal trading strategy under the GBM assumption. You will need to solve these equations to obtain the threshold levels for initiating trades. Here's a simplified outline:
State Variables: Let V(x1,x2)V(x_1, x_2)V(x1​,x2​) be the value function representing the expected profit from the pair trading strategy.
HJB Equation Formulation: Set up the HJB equations for each state of the trading position (flat, long, short).
Threshold Calculation: Use numerical methods like the Newton-Raphson method to solve for the thresholds k1,k2k_1, k_2k1​,k2​, which determine when to enter or exit trades.
Determine stop loss values
Carry out trade


https://scholarsjournal.net/index.php/ijier/article/view/3125


![gbm theory](https://github.com/user-attachments/assets/bdfe0b7e-09ae-4441-8090-5ad18ebe3381)
