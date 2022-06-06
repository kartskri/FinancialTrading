# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 22:18:09 2019
# script written to test extraction of data from bt.test
# Note that I have broken the problem down into many small pieces to solve
# one thing at a time. You should do this. 
@author: MichaelRolleigh
"""
# must import bt to use bt
import bt

# download data
data = bt.get('aapl', start='2018-01-01')


# Make a very simple strategy of holding aapl long
s = bt.Strategy('long AAPL',  [bt.algos.RunOnce(),
                              bt.algos.SelectAll(),
                              bt.algos.WeighEqually(),
                              bt.algos.Rebalance()])
# now we create the Backtest t
t = bt.Backtest(s, data)

# create results associated with that backtest t
results = bt.run(t)

# I create a DataFrame of names because I am lazy
# You can click on the DataFrame in Variable Explorer instead of looking on web
df_results_key = results.stats.assign()

# Use the stats and at attributes to get total return and save it
interesting_result_to_save = results.stats.at['total_return','long AAPL']

# Use the stats and at attributes to get daily sharpe and save it
another_interesting_result_to_save = results.stats.at['daily_sharpe','long AAPL']

# I suggest using shorter names, but I wanted this to be clear
# Look at the variable explorer or add print statements to verify that you 
#  got the stats

# You could put the above code in a loop and simply append a list or dataframe
#  with the new values every time it goes through the loop
# You could do the same with nested loops for something like short and long
#  SMA averages. Then make a heatmap and select optimal parameters!

