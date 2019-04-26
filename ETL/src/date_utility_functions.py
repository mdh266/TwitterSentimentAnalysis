import datetime

def get_day_of_week(s : str) -> str:
    """
    Converts the string from the tweets to day of week.
    """
    day      =  s[:3]
    new_day  = ""
    
    if day   == "Sun":
        new_day = "Sunday"
    elif day == "Mon":
        new_day = "Monday"
    elif day == "Tue":
        new_day = "Tuesday"
    elif day == "Wed":
        new_day = "Wednesday"
    elif day == "Thu":
        new_day = "Thursday"
    elif day == "Fri":
        new_day = "Friday"
    else:
        new_day = "Saturday"
    
    return new_day


def get_month(a : list) -> int:
    month     = a[1]
    
    if month == "Apr":
        new_month = 4
        
    elif month == "May":
        new_month = 5
        
    else:
        new_month = 6

    return new_month

def get_year(a : list) -> int:
    return int(a[-1])
    

def get_day(a : list) -> int:
    return int(a[2])


def create_timestamp(
    year  : int,
    month : int,
    day   : int,
    time  : str
	) -> datetime.datetime :
    
    t = time.split(":")
    return datetime.datetime(year, 
                             month, 
                             day, 
                             int(t[0]), 
                             int(t[1]), 
                             int(t[2]))
