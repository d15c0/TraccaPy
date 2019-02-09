#!/usr/bin/env python3

# Imports
import json
import math
import time
from time import sleep

import geopy.distance
import gpsd
import requests


def main():
    # Define globals
    global sleep_time
    global device_id
    global server
    global min_distance
    global logging
    global last_lat
    global last_lon
    global bearing

    # Open JSON(configuration) file
    with open('config.json') as json_file:
        data = json.load(json_file)

    # Set last_lat, last_lon and bearing to a string so it can be used to check if it has been changed
    bearing = last_lat = last_lon = "new"

    # Obtain values from JSON file
    sleep_time = data['sleep_time']
    device_id = str(data['device_id'])
    server = data['server']
    min_distance = data['min_distance']
    logging = data['logging']

    # Connect to gpsd
    gpsd.connect()

    # Main loop
    while 1:
        # Get current position.
        packet = gpsd.get_current()

        # Get information from gpsd
        mode = packet.mode

        # Check if fix is 3d
        if mode < 3:
            continue

        # Obtain info from gps
        lat = packet.lat
        lon = packet.lon

        # Check if it's the first run, if it is, then we can't compare to previous
        if not last_lat == "new" and not last_lon == "new":
            old = (last_lat, last_lon)
            new = (lat, lon)

            distance = geopy.distance.distance(old, new).m
            bearing = calculate_initial_compass_bearing(old, new)

            if distance <= min_distance:
                last_lat = lat
                last_lon = lon
                sleep(sleep_time)
                continue

        # Set last_lat and last_lon for distance checking
        last_lat = lat
        last_lon = lon

        # Convert to string
        lat = str(lat)
        lon = str(lon)
        bearing = str(bearing)

        # Get values from gpsd
        accuracy = str(packet.position_precision())
        alt = str(packet.alt)
        speed = str(packet.speed())

        # Initialize bearing with a standard value incase it can't be calculated
        if bearing == "new":
            bearing = "0.0"

        # Add '/' to server if it isn't included in the configuration
        first_character = ''
        if not server.endswith('/'):
            first_character = '/'

        # Set query string
        qs = first_character + "?id=" + device_id + "&timestamp=" + str(int(
            time.time())) + "&lat=" + lat + "&lon=" + lon + "&speed=" + speed + "&bearing=" + bearing + "&altitude=" + alt + "&accuracy=" + \
             str(accuracy[1]) + "&batt=100"

        # Make a POST request to the Traccar server
        post = requests.post(server + qs)
        if logging:
            if post.status_code == 200:
                print("Successfully pushed location to server (200)")
            else:
                print("Push failed (" + post.status_code + ")")

        # Sleep for the requested wait time
        sleep(sleep_time)


# Original calculate_initial_compass_bearing is found here https://gist.github.com/jeromer/2005586


def calculate_initial_compass_bearing(point_a, point_b):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(point_a) != tuple) or (type(point_b) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(point_a[0])
    lat2 = math.radians(point_b[0])

    diff_long = math.radians(point_b[1] - point_a[1])

    x = math.sin(diff_long) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(diff_long))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


if __name__ == '__main__':
    main()
