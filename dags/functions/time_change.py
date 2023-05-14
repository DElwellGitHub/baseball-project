import datetime as dt

def transform_time(orig_time):
    new_time_24_hr = dt.datetime.strptime(orig_time, '%Y-%m-%dT%H:%M:%SZ') - dt.timedelta(hours=4)
    new_time_12_hr = new_time_24_hr.strftime('%I:%M PM').lstrip('0')
    return new_time_12_hr
