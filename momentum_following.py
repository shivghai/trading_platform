#Quantopian
import numpy as np
from statsmodels import regression
import statsmodels.api as sm
import math
from operator import itemgetter

# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
def initialize(context):
    # variables
    context.shorts = []
    context.longs = []
    context.current_positions = []
    context.lookback = 250
    context.num_shorts = 1
    context.num_longs = 2
    # top 1% of stocks by volume
    set_universe(universe.DollarVolumeUniverse(99.0,100)) 
    
    
    schedule_function(rebalance, date_rule=date_rules.month_start(), time_rule=time_rules.market_open(hours=1,minutes=0))
    
# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    pass
        
def rebalance(context, data):
        prices = history(context.lookback, '1d', 'price')
        for stock in context.current_positions:
            order_target(stock, 0)
        context.current_positions = []
        for stock in prices:
            if data[stock].price > data[stock].mavg(20) + 0.5*data[stock].stddev(20):
                new = prices[stock].ix[-1]
                old = prices[stock].ix[0]
                percent_change = (new-old)/old
                context.longs.append( (stock, percent_change) )
            elif data[stock].price < data[stock].mavg(20) - 0.5*data[stock].stddev(20):
                new = prices[stock].ix[-1]
                old = prices[stock].ix[0]
                percent_change = (new-old)/old
                context.shorts.append( (stock, percent_change) )
            else:
                 pass
        context.longs = sorted(context.longs, key=itemgetter(1), reverse=True)
        context.shorts = sorted(context.shorts, key=itemgetter(1) )
        
        context.longs = context.longs[0:context.num_longs]
        context.shorts = context.shorts[0:context.num_shorts]
        
        weight = 0.20/(context.num_longs + context.num_shorts)
        
        for stock in context.longs:
                 order_target_percent(stock[0], weight)
                 context.current_positions.append(stock[0])
        for stock in context.shorts:
                 order_target_percent(stock[0], -1*weight)
                 context.current_positions.append(stock[0])