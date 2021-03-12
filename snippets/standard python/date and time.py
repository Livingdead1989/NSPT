# Use of datetime for time stamping

# from datetime import date
# print(date.today()) # Print YYYY-MM-DD

# from datetime import datetime
# print(datetime.now()) # Print YYYY-MM-DD HH:MM:SS


from datetime import datetime
now = datetime.now()
format = "%Y-%m-%d %H:%M"
time1 = now.strftime(format)
print(time1)