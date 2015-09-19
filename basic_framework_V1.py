import numpy as np
from yahoo_finance import Share
import datetime as dt
import csv

indexes_str = ['GPRO', 'T', 'C', 'DOW', 'WMT', 'AXP']
indexes = []
for index_str in indexes_str:
	indexes.append(Share(index_str))

portfolio = {}
one_year = dt.timedelta(days=100)
one_day = dt.timedelta(days=1)
today = dt.date.today()

index_counter = 0
for index in indexes:
	portfolio[indexes_str[index_counter]] = index.get_historical(str(today - one_year), str(today - one_day))
	index_counter = index_counter + 1

print ""
index_id = 0
simple_avg_num = 20
multiplier = 0.04
simple_avg = 0
exp_avg = 0

for index in indexes:
	sum_for_avg = 0
	print indexes_str[index_id]
	for x in xrange(0, simple_avg_num):
		sum_for_avg = sum_for_avg + float(portfolio[indexes_str[index_id]][x]['Adj_Close'])

	simple_avg = float(sum_for_avg/simple_avg_num)
	exp_avg = float(index.get_50day_moving_avg())
	#gets the simple average
	print "Simple: " + str(simple_avg)
	#gets the exponential average
	print "Exponential: " + str(exp_avg)

	decision = ""
	cur_price = float(index.get_price())

	if simple_avg + multiplier*cur_price < exp_avg:
		decision = "BUY"

	elif simple_avg - multiplier*cur_price > exp_avg:
		decision = "SELL"

	else:
		decision = "HOLD"

	print decision + ' ' + indexes_str[index_id] + '\n'

	index_id = index_id + 1



#print portfolio['GOOG'][0]['Date']

# temp_avg = 0
# index_string_id = 0
# offset = 0
# temp_price = 0

# for index in indexes:
# 	temp = float(index.get_200day_moving_avg())
# 	temp_price = float(index.get_price())
# 	offset = 0.2 * temp_price
# 	print '\n'
# 	print "Price: " + str(temp_price) + ", Moving Avg: " + str(temp) + ", Offset: " + str(offset)
# 	if temp > offset + temp_price:
# 		print indexes_str[index_string_id] + " is a long"
# 	elif temp + offset < temp_price:
# 		print indexes_str[index_string_id] + " is a short"
# 	else:
# 		print "Do nothing with " + indexes_str[index_string_id]
# 	index_string_id = index_string_id + 1