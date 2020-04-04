#!/usr/bin/env python3

import json
import datetime
import sys

filename = 'locations.json'

def parse_locations(locationList: list) -> list:
    parsedLocations = []
    for location in locationList:
        locationDict = {}
        fp = .0000001
        lat = int(location['latitudeE7']) * fp
        lon = int(location['longitudeE7']) * fp
        osm_url = f"https://www.openstreetmap.org/search?query={lat},{lon}#map=19"
        timestamp = int(location['timestampMs']) / 1000
        dt = datetime.datetime.fromtimestamp(timestamp).strftime('%c')
        locationDict['timestamp'] = dt
        locationDict['lat'] = lat
        locationDict['lon'] = lon
        locationDict['osm_url'] = osm_url
        parsedLocations.append(locationDict)
    return parsedLocations

def load_locations(filename: str) -> list:
    with open(filename, 'r') as file:
        locations = json.load(file)['locations']
        return locations

def run() -> None:
    print("Loading locations...", end='', flush=True)
    locations = load_locations(filename)
    print("OK!")
    print(f"Loaded {len(locations)} locations!")
    print("Parsing locations...", end='', flush=True)
    parsed_locs = parse_locations(locations)
    print("OK!")
    for loc in parsed_locs:
        print(f"Lat/Lon: {loc['lat']}, {loc['lon']}")
        print(f"Date recorded: {loc['timestamp']}")
        print(f"OpenStreetMap: {loc['osm_url']}")


if __name__ == '__main__':
    run()