import time
import datetime

print time.clock()
now = datetime.datetime.now()
print str(now)
date = '%d/%d/%d'%(now.day,now.month,now.year)
time = '%d:%d:%d'%(now.hour,now.minute,now.second)
print date
print time

print "HERE"
game_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
print game_time