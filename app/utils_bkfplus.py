import datetime

def convert_hour_minute_to_timestamp(hour, minute):

    # Get the current date
    today = datetime.date.today()

    # Create a datetime object with the specified hour and minute
    time_obj = datetime.datetime.combine(today, datetime.time(hour=hour, minute=minute))

    # Convert the datetime object to a timestamp (number of seconds since Unix epoch)
    timestamp = int(time_obj.timestamp())

    return timestamp


def convert_24_hour_time_to_12_hour_time(time:str):
    d = datetime.datetime.strptime(time, "%H:%M")
    return d.strftime("%I:%M %p")


def get_backup_file_or_directory_name(database_name):
    timestamp=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name_or_directory = f"{database_name}_backup_{timestamp}"
    return file_name_or_directory