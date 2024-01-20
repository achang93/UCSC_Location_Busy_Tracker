import googlemaps
import populartimes.populartimes as pt
import csv

# gets the data from a location given the current day and hour
# then returns a value based on busyness
def get_busy_data(current_day, current_hour, api_key, place_id):
    # dictionary of data from a given location
    # usage: get_populartimes(api_key, place_id)
    location_data = pt.get_populartimes(api_key, place_id)

    # to translate a day of week string to a number
    day_to_number = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

    # is the day of the week as an integer Monday-Friday: 0-6
    current_day = day_to_number.get(current_day)

    #in case place_id doesn't actually work
    try:
        # data for each day of the week
        # is an array of dictionaries
        all_week_data = location_data.get("populartimes")

    except:
        print("Invalid place_id: May not have data to read or doesn't exist")

    # is the data for the current day
    current_day_data = all_week_data[current_day]

    # array of numbers indicating how busy the location is at a time
    # each index represents a current hour, ex. index = 13 then it is 13:00
    #current_day_busy_data = current_day_data.get("data")

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

#returns a string based on the location, day, and time
#also returns the opening hours
def busy_and_hours(location, day, time):
    #current API key, change if needed
    api_key = 'AIzaSyAdmbXNRA37N8dkheO_6A1t2DVhTt8I4tI'

    #placeholder place_id
    place_id = 'nothing'

    #reads csv for data on location
    with open('location_ids.csv', mode='r') as file:
        csvFile = csv.reader(file)
        for location_and_place_id in csvFile:
            #location name as a string
            if location_and_place_id[0] == location:
                place_id = location_and_place_id[1]
                break

    #raise exception if the place_id isnt found
    if place_id == 'nothing':
        raise ValueError("Invalid location name:", location)

    #number based on how busy
    data = get_busy_data(day, time, api_key, place_id)

    #get opening hours, just some mumble jumble
    map_client = googlemaps.Client(api_key)
    place_details = map_client.place(place_id)
    details_results = place_details.get('result')

    #data for opening hours
    opening_hours_data = details_results['opening_hours']

    #data for each weekday
    opening_hours_times = opening_hours_data.get("weekday_text")

    #data for a specific weekday
    day_to_number = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
    opening_hours = opening_hours_times[day_to_number.get(day)]
    opening_hours = opening_hours[opening_hours.find(":") + 2:]
    open_time = opening_hours[0:opening_hours.find(":")]
    close_time = opening_hours[opening_hours.find("–") + 1: opening_hours.find(":", opening_hours.find("–"))]

    #boolean if open or not
    # REMINDER THIS IS BASED ON THE CURRENT TIME NOT A GIVEN TIME
    is_open = opening_hours_data.get("open_now")

    return check_how_busy(data), opening_hours, int(open_time), int(close_time), is_open

if __name__ == "__main__":
    busy, hours, open, close, is_open = busy_and_hours("C9/C10 Dining Hall", "Saturday", 1)