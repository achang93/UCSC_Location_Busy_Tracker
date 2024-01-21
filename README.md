# UCSC Locations
It will count and measure the amount of people in a given facility.
Shows hours of operation, if it is currently open, and how busy it is currently.
It has a UI for ease of use; just click on the location and get the most recent data.

# Front end:
To create the application for the user, we decided to use Kivy to help the user
access different locations to check the busyness and operational hours. We
implemented buttons that take the user to different locations.

# Back end:
We used the Google Maps API and Python to help gather data on how busy the location 
is at the current time and also whether it is operational at that time. We also
checked cases with respect to the time the user checked the information so we could check
whether it was opening on the same day or not. We also included a feature to tell the user
that the location will close in the next hour if the time they accessed it is within one 
hour of the closing time.

# Challenges:
- placing buttons in the proper area
- Adding images and aligning them to the corresponding buttons
- checking whether to use today's or tomorrow's operational hours with respect to the
  the time the user accessed the application
- not all locations in UCSC have the busyness feature, so the places that can be added
  are limited
- Many API calls decrease the performance of the application, so there is a 1-2 second
  delay after pressing a button

# Future Work:
- Add more features from the Google API into the application to help the user obtain
  more information about the location
- Decrease the execution time of each API call so that the user experience is smoother
- Add more UCSC locations that have or do not have the busyness feature, and then can be
  implemented if it does have that feature
