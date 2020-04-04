#!/usr/bin/env python3

import json
import datetime
import sys

filename = 'locations.json'

class LocationsException(Exception): pass
class Locations:

    def __init__(self, filename):
        self.filename = filename
        self.locations_raw = None
        self.locations = None

        try:
            self._load_locations()
            self._parse_locations()
        except Exception as e:
            raise LocationsException(str(e))

    def getLocationsByYear(self, year: str) -> list:
        locs = []
        for location in self.locations:
            if location['timestamp'].strftime('%Y') == str(year):
                locs.append(location)
        return locs

    def saveToDB(self) -> bool:
        return False

    def _parse_locations(self, locationList: list) -> list:
        parsedLocations = []
        for location in self.locations_raw:
            locationDict = {}
            fp = .0000001
            lat = int(location['latitudeE7']) * fp
            lon = int(location['longitudeE7']) * fp
            osm_url = f"https://www.openstreetmap.org/search?query={lat},{lon}#map=19"
            timestamp = int(location['timestampMs']) / 1000
            dt = datetime.datetime.fromtimestamp(timestamp)
            locationDict['timestamp'] = dt
            locationDict['lat'] = lat
            locationDict['lon'] = lon
            locationDict['osm_url'] = osm_url
            parsedLocations.append(locationDict)
        self.locations = parsedLocations

    def _load_locations() -> list:
        with open(filename, 'r') as file:
            locations = json.load(file)['locations']
            self.locations_raw = locations

def run() -> None:
    locs = Locations(filename)
        locations = load_locations(filename)
                parsed_locs = parse_locations(locations)
        for loc in parsed_locs:
                        

if __name__ == '__main__':
    run()