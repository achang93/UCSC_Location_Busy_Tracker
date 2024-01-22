import googlemaps
import populartimes.populartimes as pt
import datetime


# gets the data from a location given the current day and hour
# then returns a value based on busyness
def get_busy_data(current_day, current_hour, api_key, place_id):
    # dictionary of data from a given location
    # usage: get_populartimes(api_key, place_id)
    location_data = pt.get_populartimes(api_key, place_id)


    # is the day of the week as an integer Monday-Friday: 0-6
    if not isinstance(current_day, int):
        raise ValueError("Invalid day")

    # in case place_id doesn't actually work
    try:
        # data for each day of the week
        # is an array of dictionaries
        all_week_data = location_data.get("populartimes")

    except:
        print("Invalid place_id: May not have data to read or doesn't exist")

    # is the data for the current day
    if current_day == 6:
        current_day_data = all_week_data[6]
    else:
        current_day_data = all_week_data[current_day]
    
    # data on the current hour
    current_hour_data = current_day_data.get("data")[current_hour]

    return current_hour_data


# accesses data from the hour to find out how relatively busy it is
def check_how_busy(data):
    if (data == 0):
        return "Closed"

    if (data < 25):
        return "Not that busy"

    if (data < 50):
        return "Not too busy"

    if (data < 75):
        return "A little busy"

    else:
        return "Busy"


# returns a string based on the location, day, and time
# also returns the opening hours
def busy_and_hours(location):
    time = int(datetime.datetime.now().strftime("%H"))
    day = int(datetime.datetime.today().weekday())

    # current API key, change if needed
    api_key = 'AIzaSyAdmbXNRA37N8dkheO_6A1t2DVhTt8I4tI'

    # place_id dictionary
    place_ids = {"McHenry Library": "ChIJk7eypKFBjoAR87wpNgAjQek",
                 "Fitness Center": "ChIJVRW6fKRBjoARlWkP543vP7g",
                 "Bay Tree Campus Store": "ChIJmWae1aBBjoARhPuzroaHOxg",
                 "Science and Engineering Library": "ChIJWeGcqQpBjoARohHiF-L7tB0"}

    # raise exception if the place_id isnt found
    try:
        place_id = place_ids.get(location)
    except:
        raise ValueError("Invalid location")

    # number based on how busy
    data = get_busy_data(day, time, api_key, place_id)

    if (data == 0):
        if day < 6:
            day = day + 1
        else:
            day = 0

    # get opening hours, just some mumble jumble
    map_client = googlemaps.Client(api_key)
    place_details = map_client.place(place_id)
    details_results = place_details.get('result')

    # data for opening hours
    opening_hours_data = details_results['opening_hours']
    print(details_results)
    is_open = opening_hours_data.get("open_now")

    # data for each weekday
    opening_hours_times = opening_hours_data.get("weekday_text")

    opening_hours = opening_hours_times[day]


    #if "Closed" in opening_hours:
    #    print("it went here")
    #    return check_how_busy(data), opening_hours[opening_hours.find("Closed"):], is_open, 0


    opening_hours = opening_hours[opening_hours.find(":") + 2:]
    opening_hours = ''.join(s for s in opening_hours if ord(s)>31 and ord(s)<126)
    opening_hours = opening_hours[0:opening_hours.find("M") + 1] + "-" + opening_hours[opening_hours.find("M") + 1:]

    # following code is to check whether the location closes in 1 hr or less
    y = opening_hours[opening_hours.find("M") + 1:]
    ending = opening_hours[-2:]
    y = str(y)
    y = y[1:]
    x = 0
    for i in range(len(y)):
        if y[i] == ':':
            break
        else:
            x += 1
    y = y[:x]

    if ending == 'PM':
        y = int(y) + 12
    # bottom if statement is to check whether it is 1 hr away from closing
    if y == "Open 24 hours":
        print("it went here1")
        return check_how_busy(data), "Open 24 hours", is_open, 0

    if int(y) - int(datetime.datetime.now().strftime("%H")) == 1:
        print("it went here2")
        return check_how_busy(data), opening_hours, is_open, 1

    print("it went here3")
    #print(time)
    #print(day)

    return check_how_busy(data), opening_hours, is_open, 0

def open_close(check_next, busy, hours, is_open, case):
    if is_open:
        if case == 1:

            if check_next + 1 == 13:
                check_next = 1
            ending = hours[-2:]
            hours = "Closing at " + str(check_next + 1) + ":00 " + ending
            return f'Open\n{busy}\n{hours}'
        else:
            return f'Open\n{busy}\n{hours}'
    else:
        if check_next < 12:
            return f"Closed\nToday's hours: {hours}"
        else:
            return f"Closed\nTomorrow's hours: {hours}"


def check_UCSC_fitness():

    busy, hours, is_open, case = busy_and_hours("Fitness Center")
    check_next = int(datetime.datetime.now().strftime("%H"))

    return open_close(check_next, busy, hours, is_open, case)
    


def check_UCSC_mchenry():
    #print("mchenry")
    busy, hours, is_open, case = busy_and_hours("McHenry Library")
    check_next = int(datetime.datetime.now().strftime("%H"))

    return open_close(check_next, busy, hours, is_open, case)



def check_UCSC_sne():
    #print("sne")
    busy, hours, is_open, case = busy_and_hours("Science and Engineering Library")
    check_next = int(datetime.datetime.now().strftime("%H")) 
    
    return open_close(check_next, busy, hours, is_open, case)

def check_UCSC_baytree():
    busy, hours, is_open, case = busy_and_hours("Bay Tree Campus Store")
    check_next = int(datetime.datetime.now().strftime("%H"))
    #print(datetime.datetime.today().weekday())
    if int(datetime.datetime.today().weekday()) == 5:
        return f'Closed\nTomorrow\'s hours: Closed'
    if int(datetime.datetime.today().weekday()) == 6:
        return f'Closed\nTomorrow\'s hours: {hours}'
    if is_open:
        if case == 1:
            if check_next+1 == 13:
                check_next = 1
            ending = hours[-2:]
            hours = "Closing at " + str(check_next+1) + ":00 " + ending
            return f'Open\n{busy}\n{hours}'
        else:
            return f'Open\n{busy}\n{hours}'
    else:
        if check_next < 12:
            return f"Closed\nToday's hours: {hours}"
        else:
            return f"Closed\nTomorrow's hours: {hours}"

if __name__ == "__main__":
    busy, hours, is_open, val = busy_and_hours("McHenry Library")
    #print(busy, hours, is_open, val)
    print(check_UCSC_mchenry())