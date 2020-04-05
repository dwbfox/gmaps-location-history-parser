#!/usr/bin/env python3

import argparse
import json
import datetime
from prettytable import PrettyTable

class LocationsException(Exception):
    pass


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

    def _parse_locations(self) -> list:
        parsedLocations = []
        for location in self.locations_raw:
            locationDict = {}
            fp = .0000001
            lat = int(location['latitudeE7']) * fp
            lon = int(location['longitudeE7']) * fp
            osm_url = f"http://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=12"
            timestamp = int(location['timestampMs']) / 1000
            dt = datetime.datetime.fromtimestamp(timestamp)
            locationDict['timestamp'] = dt
            locationDict['lat'] = lat
            locationDict['lon'] = lon
            locationDict['osm_url'] = osm_url
            parsedLocations.append(locationDict)
        self.locations = parsedLocations

    def gen_table(self, header: str, rows: list):
        table = PrettyTable()
        table.field_names = header
        for row in rows:
            table.add_row([f"{row['lat']},{row['lon']}", row['timestamp'], row['osm_url']])
        return table

    def _load_locations(self) -> list:
        with open(self.filename, 'r') as file:
            locations = json.load(file)['locations']
            self.locations_raw = locations


def run() -> None:
    parser = argparse.ArgumentParser(description='Parse and output Google Maps location history JSON data')
    parser.add_argument('--file', dest='filename', help='The Google Maps history JSON file to parse', required=True)
    parser.add_argument('--month', dest='month',
        choices=['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        help='Filter output by year of data acquisition',
        required=False
    )
    parser.add_argument('--year', dest='year', type=int, help='Filter output by year of data acquisition', required=False)

    args = parser.parse_args()

    locs = Locations(args.filename)
    print(locs.gen_table([
        "Lat/Lon",
        "Date",
        "OpenStreetMap"
    ], locs.getLocationsByYear(args.year)))


if __name__ == '__main__':
    run()
