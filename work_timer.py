import re
from datetime import datetime, timedelta

input_string = """
Time Events
Event Type
Date & Time
Status
Clock-in	
19.06.2023
08:44:15
Posted		
Clock-out	
19.06.2023
18:08:32
Posted		
Time Events
Event Type
Date & Time
Status
Clock-in	
20.06.2023
08:34:20
Posted		
Clock-out	
20.06.2023
18:10:50
Posted		Time Events
Event Type
Date & Time
Status
Clock-in	
21.06.2023
08:39:15
Posted		
Clock-out	
21.06.2023
16:56:09
Posted		


"""


def print_last_element(days_work_time):
    if len(days_work_time) == 0:
        return
    if days_work_time[-1].total_seconds() / 3600 < 8:
        flag = 'Need'
        diff_eight_hours = timedelta(hours=8) - days_work_time[-1]
    else:
        flag = 'Extra'
        diff_eight_hours = days_work_time[-1] - timedelta(hours=8)
    print(f'Work: {days_work_time[-1]}, {flag} {diff_eight_hours}')


timestamps = re.findall(r'\d{2}:\d{2}:\d{2}', input_string)
dates = re.findall(r'\d{2}\.\d{2}\.\d{4}', input_string)

timestamp_pairs = [timestamps[i:i + 2] for i in range(0, len(timestamps), 2)]
date_pairs = [dates[i:i + 2] for i in range(0, len(dates), 2)]

days_work_time = []

for i, pair in enumerate(timestamp_pairs):
    start_time = datetime.strptime(pair[0], '%H:%M:%S')
    end_time = datetime.strptime(pair[1], '%H:%M:%S')
    time_diff = end_time - start_time
    # day_total_time += time_diff.total_seconds()

    if date_pairs[i][0] == date_pairs[i][1]:
        if date_pairs[i - 1][0] == date_pairs[i][0]:
            days_work_time[-1] += time_diff
        else:
            print_last_element(days_work_time)
            days_work_time.append(time_diff)

print_last_element(days_work_time)
# total_time_in_hours = total_time / 3600
# print(f'\nTotal time: {total_time_in_hours} hours')

# Calculate working hours for the current day of the week
current_day = datetime.now().weekday()
accmulated_work_hours = sum(i.total_seconds() for i in days_work_time) / 3600

print(f'Have worked {accmulated_work_hours:.2f} hours so far')

hours_to_work = 8 * (current_day + 1) - accmulated_work_hours

if hours_to_work < 0:
    print(f'Overworked by {-hours_to_work:.2f} hours')
else:
    print(f'Need to work {hours_to_work:.2f} hours')

current_time = datetime.now()
time_to_leave = current_time + timedelta(hours=hours_to_work)
print(f'You can leave at {time_to_leave.strftime("%H:%M:%S")}')