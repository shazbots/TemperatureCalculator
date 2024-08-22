# TemperatureCalculator
A side project to practice cURL commands and polars dataframes, along with other Python libraries.
This program will calculate the current average temperature of various US capital cities, based on the starting letter of state's name.

## Description:
This Python code will calculate the average temperatures of multiple state capitals, based on the starting letter of a state's name. For example, if you enter the letter "C", you will calculate the current average temperatures of:
- Sacramento, California
- Denver, Colorado

The temperatures are being pulled from the openweathermap.org API.
The states and capitals csv was originally from https://github.com/jasperdebie/VisInfo/blob/master/us-state-capitals.csv however, I had to make some modifications to that file, because of "unclean text", like `<BR>` at the end of some location names.
The final temperature result will be truncated to the nearest **tenth** of a degree.

### Dependencies
* This program was ran on Python 3.12
* It uses the following libraries:
  * argparse
  * configparser
  * numpy
  * polars
  * requests

### Executing the Program
* Before executing the program, make sure you have put the `config.ini` file in the same directory as the `TemperatureCalculator.py` file. Make sure to have the appropriate settings for the file:
 * `debug` - (Boolean) This setting is for verbose logging to view additional log output.
 * `fahrenheit` - (Boolean) This is for the temperature units. Setting this to False will make things in Celsius.
 * `api_key` - (String) This is the Openweathermap API. You will need to register for a key if you do not have one. (openweathermap.org)
* To execute the program, type the following:
```<python> TemperatureCalculator --startingletter <letter>```
Where `<python>` is whatever command you type to start your python interpreter, and `<letter>` is the starting letter for whichever states you want to use. Note that it is *case insensitive*.

## License
This project is licensed under the MIT License License - see the LICENSE.md file for details.
