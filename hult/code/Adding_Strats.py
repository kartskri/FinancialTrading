# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 00:38:59 2019

This scripts shows how to add additional strats to a backtest, plots, and results

@author: MichaelRolleigh
"""

import bt


# Fetch some data
data = bt.get('spy,agg', start='2010-01-01')

# Recreate the strategy named First_Strat
First_Strat = bt.Strategy('First Strat', [bt.algos.RunMonthly(),
                                     bt.algos.SelectAll(),
                                     bt.algos.WeighEqually(),
                                     bt.algos.Rebalance()])

# Create a backtest named test
test = bt.Backtest(First_Strat, data)

# create a second strategy named Second_Strat
# Note only difference from First_Strat is that we RunWeekly and Weight using Inverse Volatility
# This means the strategy will make more trades and put more weight on less Volatile asset
Second_Strat = bt.Strategy('Second Strat', [bt.algos.RunWeekly(),
                        bt.algos.SelectAll(),
                        bt.algos.WeighInvVol(),
                        bt.algos.Rebalance()])

# Test Second_Strat and name it test2
test2 = bt.Backtest(Second_Strat, data)

# To see the results side-by-side, we must tell the bt.run to use both tests
# All res2 commands will produce output comparing s1 and s2 because we have test and test2
results_both = bt.run(test, test2)

# res_First_Strat only has test in it, so you will only see Second_Strat from it
res_First_Strat = bt.run(test)

# res_Second_Strat only has test2 in it, so you will only see Second_Strat from it
res_Second_Strat = bt.run(test2)

# res2 plots here include both s1 and s2 info
results_both.plot()

results_both.display()

# Plot weights from the first strategy to illustrate the different weighting schemes
res_First_Strat.plot_security_weights()
res_Second_Strat.plot_security_weights()
# For some reason, I cannot plot weights or histograms for both at the same time
results_both.plot_security_weights()







