# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 22:33:04 2019

Showing looping with bt.py 

This is a very inelegant way of looping. I did it this way to make it very 
clear what was going on and how it relates to the steps described in class. 
It is often useful to start with an inelegant program when you are trying new
things. It is also often useful to code something 'quick and dirty' when you 
have a limited time to work on it.

@author: MichaelRolleigh
"""
# import pandas 
import pandas as pd
# must import bt to use bt
import bt

"""
 Use custom function to make it easier to repeatedly use the same strat
 Note how I changed the start date so that it was very short to make program
  run faster while debugging.  
"""
def above_sma(tickers, sma_per=50, start='2015-01-01', name='above_sma'):
    """
    Long securities that are above their n period
    Simple Moving Averages with equal weights.
    """
    # download data
    data = bt.get(tickers, start=start)
    # calc sma
    sma = data.rolling(sma_per).mean()

    # create strategy
    s = bt.Strategy(name, [bt.algos.SelectWhere(data > sma),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()])

    # now we create the backtest
    return bt.Backtest(s, data)


# Create a result_df to store results
result_df = pd.DataFrame(columns = ['SMA','CAGR','daily_sharpe'])

# Our simple investment universe 
tickers = 'goog,AAPL,msft'
"""
 Loop over SMA_number; It would be more elegant to define an object at the top
 including SMA and loop over that column. That is more pythony. This 'for in range'
 style is more like the math books on numerical recipes. It is sometimes useful to 
 write things this way to link it more easily with the model in your mind.
"""

for SMA_number in range(10,20): 
    # create a string that is the name of our SMA strategy
    SMA_name='sma'+ str(SMA_number)
    # generate result feeding the above_sma function variables that change in the loop
    result = bt.run(above_sma(tickers, sma_per=SMA_number, name= SMA_name))

    # There is a more elegant way to do this, but this works
    result_df = result_df.append({'SMA':SMA_number,'CAGR':result.stats.at['cagr',SMA_name], 
                                  'daily_sharpe': result.stats.at['daily_sharpe',SMA_name]},ignore_index=True)
   

# Set the index to SMA. The other arguments are there because StackOverflow suggested them and they work
result_df.set_index('SMA',inplace=True, drop=True)


