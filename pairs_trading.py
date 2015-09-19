#Quantopian

import numpy as np
from statsmodels import regression
import statsmodels.api as sm
import math

# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
def initialize(context):
    # variables
    context.stocks = set()
    context.lookback = 100
    context.longs = set()
    context.shorts = set()
    # top 1% of stocks by volume
    set_universe(universe.DollarVolumeUniverse(99.0,100)) 
    # commission for Interactive Brokers
    set_commission(commission.PerShare(cost=0.0075, min_trade_cost=1.00))
    # set slippage according to sample
    set_slippage(slippage.VolumeShareSlippage(volume_limit=0.025, price_impact=0.10))
    
    schedule_function(rebalance, 
                      date_rules.week_start(days_offset=0),
                      time_rules.market_open(hours = 0, minutes = 1)) 
# Will be called on every trade event for the securities you specify. 
def handle_data(context, data):
    log.info(str(context.portfolio.portfolio_value) )
    prices = history(context.lookback, '1d', 'price')
    for stock1 in prices:
        for stock2 in prices:
            if stock1 == stock2:
                pass
            else:
                arr1 = []
                arr2 = []
                for x in prices[stock1]:
                    arr1.append(x)
                for x in prices[stock2]:
                    arr2.append(x)
                if(abs(np.corrcoef(arr1, arr2)[0][1]) > 0.97):
                    if( stock1 < stock2 ):
                        context.stocks.add((stock1, stock2))
                    else:
                        context.stocks.add((stock2, stock1))
    
    # Implement your algorithm logic here.
    # data[sid(X)] holds the trade event data for that security.
    # context.portfolio holds the current portfolio state.

    # Place orders with the order(SID, amount) method.

    # TODO: implement your own logic here.
    
def rebalance(context, data):
    # delete all previous values
    for stock1, stock2 in context.stocks:
        mavg1 = data[stock1].mavg(10)
        mavg2 = data[stock2].mavg(10)
        stddev1 = data[stock1].stddev(10)
        stddev2 = data[stock2].stddev(10)
        
        log.info( str(stock1) + ' ' + str(stock2) )
        
        if data[stock1].price - 0.5*stddev1 > mavg1 and  mavg2 + 0.5*stddev2 < data[stock2].price:
            if stock1 in context.shorts or stock2 in context.longs:
                order_target(stock1, 0)
                order_target(stock2, 0)
                context.shorts.discard(stock1)
                context.longs.discard(stock2)
            else:
                order_target_value(stock1, -100000)
                order_target_value(stock2, 100000)
                context.shorts.add(stock1)
                context.longs.add(stock2)
                
        elif data[stock2].price - 0.5*stddev2 > mavg2 and  mavg1 + 0.5*stddev1 < data[stock1].price:
            if stock1 in context.longs or stock2 in context.shorts:
                order_target(stock1, 0)
                order_target(stock2, 0)
                context.longs.discard(stock1)
                context.shorts.discard(stock2)
            else:
                order_target_value(stock1, 100000)
                order_target_value(stock2, -100000)
                context.longs.add(stock1)
                context.shorts.add(stock2)
        else:
            context.longs.discard(stock1)
            context.shorts.discard(stock1)
            context.longs.discard(stock2)
            context.shorts.discard(stock2)
            order_target(stock1, 0)
            order_target(stock2, 0)
    context.stocks = set()
    