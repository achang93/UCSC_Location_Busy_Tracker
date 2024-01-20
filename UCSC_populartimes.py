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
                 "SNE Library": "ChIJWeGcqQpBjoARohHiF-L7tB0"}

    # raise exception if the place_id isnt found
    try:
        place_id = place_ids.get(location)
    except:
        raise ValueError("Invalid location")

    # number based on how busy
    data = get_busy_data(day, time, api_key, place_id)

    # get opening hours, just some mumble jumble
    map_client = googlemaps.Client(api_key)
    place_details = map_client.place(place_id)
    details_results = place_details.get('result')

    # data for opening hours
    opening_hours_data = details_results['opening_hours']

    # data for each weekday
    opening_hours_times = opening_hours_data.get("weekday_text")

    opening_hours = opening_hours_times[day]
    opening_hours = opening_hours[opening_hours.find(":") + 2:]

    # boolean if open or not
    # REMINDER THIS IS BASED ON THE CURRENT TIME NOT A GIVEN TIME
    is_open = opening_hours_data.get("open_now")

    return check_how_busy(data), opening_hours, is_open


if __name__ == "__main__":
    busy, hours, is_open = busy_and_hours("McHenry Library")
    print(busy, hours, is_open)