#!/usr/bin/python
# -*- coding: utf-8 -*-
#######################
##
##  WUtemp.py
##  Updates Conky with temperature from WeatherUnderground
##
##  by Doyousketch2
##  Nov 4, 2016
##
##  GNU GPLv3 - https://www.gnu.org/licenses/gpl-3.0.html
##
##########################################
##
##  Place WUtemp.py script in your Conky config dir.
##  ~/.config/conky/
##
##  make sure you can run it:
##  chmod 770 ScratchMessages.py
##
##  Add the next line to your ~/.config/conky/conky.conf
##----------------------------------------------------------
##
##  ${execpi 1800 python ~/.config/conky/WUtemp.py}
##
##----------------------------------------------------------
##  And place it under the part that says:  conky.text = [[
##
##  Script updates every 1800 sec's.
##  Divide by 60 to get mins, so 30 mins.
##
##########################################
##
##  If you don't have PIP:
##  sudo apt-get install pip
##
##  If you don't have the REQUESTS module:
##  pip install requests
##
##########################################
##########################################
##  set variables here:

##  Get your free WeatherUnderground key from:
##  https://www.wunderground.com/weather/api
##  key limit: up to 500 calls per day, 10 per min.
KEY = '123456789'

##  set degrees to 'F' or 'C'
DEGREES = 'C'

##  set your city here:
CITY = ''

##  number of tries before it gives up:
ATTEMPTS = 3

##  Message if server not found:
NADA = 'WU server not found...'

##  standard websafe hex colors.
##  #RRGGBB  or #RGB format, so...

##  FFFFFF  or  FFF  =  white
##  FF0000  or  F00  =  red
##  00FF00  or  0F0  =  green
##  0000FF  or  00F  =  blue
##  000000  or  000  =  black

Color1 = 'e74c3c'
Color2 = '2980b9'
Color3 = 'bdc3c7'

##  Font size for temperature:
BOLD = '${font :style=Bold:pixelsize=15}'

##########################################
##  Don't edit code below.
##
##  example URL's ########################
##  http://mobile.wunderground.com/cgi-bin/findweather/getForecast?brand=mobile_english&query=12345
##  http://mobile.wunderground.com/cgi-bin/findweather/getForecast?brand=mobile_metric&query=12345
##  https://mobile.wunderground.com/cgi-bin/findweather/getForecast?query=12345
##
##  http://api.wunderground.com/api/1234567812345678/conditions/q/CA/12345.json
##########################################

import requests as RQ  ##  used to access URL's in Python
import time  ##  used to delay a moment between server retries

##  put color codes in a format Conky can decode.
C1 = '${color ' + Color1 + '}'
C2 = '${color ' + Color2 + '}'
C3 = '${color ' + Color3 + '}'

def CheckIt(ZIP):  ##  simple function to check server.

	Response = RQ .get('http://api.wunderground.com/api/' + KEY + '/conditions/q/TR/' + CITY + '.json')
	##  Expect a response like:   {"response": ...}
	##  Convert this from json string to python dictionary.
	Dict = Response .json()

	try:  ##  get values contained within the 'current_observation' key.
		Current = Dict['current_observation']

		TempF = str(Current['temp_f'])
		TempC = str(Current['temp_c'])

		Humid = str(Current['relative_humidity'])
		WindMPH = str(Current['wind_mph'])
		WindKPH = str(Current['wind_kph'])

		FeelsF = str(Current['feelslike_f'])
		FeelsC = str(Current['feelslike_c'])

		##  convert to integer, so we can compare numbers
		if '.' in FeelsF:  ##  if it has a decimal,
			intF = int(FeelsF .split('.')[0])  ## let's strip that.

		else:  ##  if temp doesn't have a decimal, we can just use that.
			intF = int(FeelsF)

		##  get numerical value for humidity, and strip trailing % sign
		intH = int(Humid .split('%')[0])
		##  blue hue for humidity value
		BlHue = intH * 2 + 55

		##  red temperature value
		if intF > 85:
			R = 255
		elif intF > 32:
			R = (intF * 3) - 15
		else:
			R = 0

		##  green temperature value
		if intF > 32:
			G = intF + 20
		else:
			G = 30

		##  blue temperature value
		if intF > 85:
			B = intF * 2
		elif intF < 1:
			B = 255
		else:
			B = 255 - (intF * 3)

		##  convert RGB values to hex
		##  example:  hex(255) = 0xff

		hexR = hex(R) .split('x')[1]  ##  split at the ('x') and only use the hex digits after that 'x'
		if len(hexR) < 2: hexR = ('0' + hexR)  ## make sure we have 2 digits.

		hexG = hex(G) .split('x')[1]  ##  same thing for green.
		if len(hexG) < 2: hexG = ('0' + hexG)

		hexB = hex(B) .split('x')[1]  ##  same thing for blue.
		if len(hexB) < 2: hexB = ('0' + hexB)

		hexBl = hex(BlHue) .split('x')[1]  ##  same thing for humidity blue.
		if len(hexBl) < 2: hexBl = ('0' + hexBl)

		##  concatenate the results.
		Tmp = '${color ' + hexR + hexG + hexB + '}'
		Hue = '${color 0050' + hexBl + '}'

		##  print °F response
		if DEGREES == 'F':
			if TempF == FeelsF:  ##  if it feels exactly like actual temp, we don't need to print both.
				print(BOLD + Tmp + FeelsF + '°${font}F  ' + Hue + Humid + '  ' + C2 + WindMPH + C3 + 'mph ')

			else:  ##  if temp feels diff then actual, print both and color how it feels.
				print(C1 + TempF + '°F  ' + Hue + Humid + '  ' + C3 + WindMPH + 'mph  ' + Tmp + BOLD + FeelsF + '°${font}F')

		##  or print °C response
		elif DEGREES == 'C':
			if TempC == FeelsC:  ##  if it feels exactly like actual temp, we don't need to print both.
				print(BOLD + Tmp + TempC + '°${font}C  ' + Hue + Humid + '  ' + C2 + WindKPH + C3 + 'kph')

			else:  ##  if temp feels diff then actual, print both and color how it feels.
				print(C1 + TempC + '°C  ' + Hue + Humid + '  ' + C3 + WindKPH + 'kph  ' + Tmp + BOLD + FeelsC + '°${font}C')

	except:  ##  if we didn't get current info,
		Error = Dict['error']  ##  check for an error response.
		errorType = str(Error['type'])
		print(errorType)  ##  and let us know what it was.


##########################################
##  function defined.  ok, go.

attempt = 0
while attempt < ATTEMPTS:  ##  simple retry loop
	try:
		CheckIt(CITY)  ##  check our zipcode
		attempt = ATTEMPTS  ##  we don't need to keep trying if we got a response.

	except:  ##  if no response
		attempt += 1  ##  keep track of tries
		time.sleep(0.2)  ##  wait a moment before trying again.

		if attempt == ATTEMPTS:  ##  if all else fails,
			print(NADA)  ##  print our generic error response.

print('') ##  print a blank line at the end, so it's easy to read on Conky
