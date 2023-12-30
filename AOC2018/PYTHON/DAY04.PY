#=============================================================
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
daytext = os.path.basename(__file__)[3:5] # Get the day number as two digits from the 3rd and 4th characters of the script filename
file_path = os.path.join(script_dir, f"day{daytext}.txt")
text = open(file_path).read()
#=============================================================
from datetime import datetime, timedelta
from collections import defaultdict
lines = text.split('\n')
lines.sort()

# [1518-03-11 00:01] Guard #1091 begins shift
# [1518-03-22 00:29] falls asleep
# [1518-09-26 00:59] wakes up
guard_to_date = defaultdict()
def defdic():
    return []
events = defaultdict(defdic)

thisguard = None
for line in lines:
    bits = line.split("]")
    datetimestr = bits[0][1:]
    datetim = datetime.strptime(datetimestr, '%Y-%m-%d %H:%M') + timedelta(hours=1)
    date = datetim.date()
    mins = int(datetimestr[11:13]) * 60 + int(datetimestr[14:16])
    
    words = bits[1].strip().split(' ')
    if words[0] == 'Guard':
        thisguard = int(words[1][1:])
        guard_to_date[date] = thisguard
    elif words[0] == 'falls':
        events[date].append(mins)
    elif words[0] == 'wakes':
        events[date].append(mins)

def zero(): return 0
guardmins = defaultdict(zero)
for date, guard in guard_to_date.items():
    # print("---------")
    changes = [mins for mins in events[date]]
    changes.sort()
    changestuples = [(changes[index],changes[index+1]) for index in range(0, len(changes),2)]
    mins = sum([changes[index+1]-changes[index] for index in range(0, len(changes),2)])
    # print(guard, date)
    # print(changes, mins)
    guardmins[guard] += mins

maxmins = 0
maxminguard = None
for guard, mins in guardmins.items():
    if mins > maxmins:
        maxmins = mins
        maxminguard = guard
# We've established maxminguard
# Now need to find the minute when that guard is most asleep

print("MaxMinute guard = ", maxminguard, "with a total of ", maxmins, "minutes")

# Set up a counter for each minute of the hour
minsofhour = defaultdict(zero)
for date, guard in guard_to_date.items():
    changes = [mins for mins in events[date]]
    changes.sort()
    changestuples = [(changes[index],changes[index+1]) for index in range(0, len(changes),2)]
    for changefrom, changeto in changestuples:
        for min in range(changefrom, changeto):
            minofhour = min % 60
            minsofhour[(guard, minofhour)] += 1

maxmincount = 0
maxmin = None
maxminanycount = 0
maxminany = None
maxminanyguard = None
for (guard, min), mincount in minsofhour.items():
    if mincount > maxminanycount:
        maxminanycount = mincount
        maxminany = min
        maxminanyguard = guard
    if guard == maxminguard:
        if mincount > maxmincount:
            maxmincount = mincount
            maxmin = min
print("Minute for which that guard is most asleep is:", maxmin)
print("Result A = ", maxminguard*maxmin)
print("Guard asleep in one minute more than any other is:", maxminanyguard)
print("Minute for which that guard is most asleep is:", maxminany)
print("Result B = ", maxminanyguard*maxminany)
