import argparse
import configparser
import numpy as np
import polars as pl
import requests

class TemperatureCalculator:

    # init method or constructor
    def __init__(self):

        # Read Configuration File
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.debug = config.getboolean('Settings', 'debug')
        self.fahrenheit = config.getboolean('Settings', 'fahrenheit')
        self.api_key = config.get('Settings', 'api_key')

        self.printDebugMessage(self.debug)
        self.printDebugMessage(self.fahrenheit)
        self.printDebugMessage(self.api_key)

        # Get starting letter from command line input
        parser = argparse.ArgumentParser()
        parser.add_argument("--startingletter", type=str)
        args = parser.parse_args()

        self.printDebugMessage(f'Starting Letter: {args.startingletter}')

        # Error Checking for input
        if len(args.startingletter) == 1 and args.startingletter.isalpha():
            print(f'Finding states that start with character: "{args.startingletter}".')
        else:
            print(f'Invalid input detected: "{args.startingletter}". Please enter a single letter. (Case-insensitive)')
            exit()

        self.starting_letter = args.startingletter

        # Read states & capitals CSV file.
        self.us_state_capitals_df = pl.read_csv('us-state-capitals.csv')

    def printDebugMessage(self, message, indents=0):
        if self.debug:
            print(f'{indents*"\t"}[DEBUG] - {message}')

    def get_capitial_cities_starting_with_letter(self):
        df = self.us_state_capitals_df.select(pl.col('state'), pl.col('capital')) \
            .filter((pl.col('state').str.to_uppercase()) \
                .str.starts_with(self.starting_letter.upper()))

        return df.rows(named=False)

    def get_current_temp(self, lat, lon, units):
        payload = {
            'lat': lat,
            'lon': lon,
            'units': units,
            'appid': self.api_key
        }

        r = requests.get('https://api.openweathermap.org/data/2.5/weather',
                         params=payload)
        return r.json()['main']['temp']

    def get_lat_lon(self, city, state):
        payload = {
            'q': f'{city}, {state}, US',
            'limit': 10,
            'appid': self.api_key
        }

        r = requests.get('http://api.openweathermap.org/geo/1.0/direct',
                         params=payload)

        return r.json()[0]['lat'], r.json()[0]['lon']

    def run_program(self):
        states_and_capitals_list = self.get_capitial_cities_starting_with_letter()

        self.printDebugMessage('States and Capitals List:')
        self.printDebugMessage(states_and_capitals_list)

        if not states_and_capitals_list:
            print("No states found with that letter.")
            exit()

        self.printDebugMessage(f'{len(states_and_capitals_list)} entries found')

        temp_list = []

        self.printDebugMessage('Listing All Cities')

        # Get the temperatures and average them
        for state, capital in states_and_capitals_list:
            lat, lon = self.get_lat_lon(capital, state)
            temperature_unit_string = 'imperial' if self.fahrenheit else 'metric'
            current_temp = self.get_current_temp(lat, lon, temperature_unit_string)

            self.printDebugMessage(f'{capital}, {state}: {current_temp:.1f}{"ºF" if self.fahrenheit else "ºC"}', indents=1)
            temp_list.append(current_temp)

        print(f'\nAverage Temperature: {np.mean(temp_list):.1f}{"ºF" if self.fahrenheit else "ºC"}')


if __name__ == '__main__':
    t = TemperatureCalculator()
    t.run_program()