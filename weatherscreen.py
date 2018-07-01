#!/usr/bin/python3

# 
# A python script that prints temperature, weather forecast and time on a Inky pHAT (212x104 pixel) screen.
#
# Weather forecast from Yr, delivered by the Norwegian Meteorological Institute and NRK
#

from datetime import datetime
import time
import inkyphat
from PIL import ImageFont
from PIL import Image
import json
import requests
from xml.dom import minidom

# Domoticz temperature sensor facing west
TEMP_SENSOR_1 = 4
# Domoticz temperature sensor facing north
TEMP_SENSOR_2 = 156
# store three forecasts
weather_forecasts = [None] * 3
# call service every 15 minutes
weather_forecast_counter = 15

def write_time(inkyphat):
	current = datetime.now().strftime('%H:%M')	
	time_font = ImageFont.truetype(inkyphat.fonts.PressStart2P, 20)
	w, h = time_font.getsize(current)
	x = inkyphat.WIDTH - w
	y = inkyphat.HEIGHT - h
	inkyphat.text((x, y), current, inkyphat.BLACK, time_font)
	return
	
def get_sensor_data(id):
	try:
		# get from Domoticz
		r = requests.get('http://<domoticz_address>:8080/json.htm?type=devices&rid=' + str(id), timeout=3)
		# parse JSON
		data = json.loads(r.text)
		temperature = data['result'][0]['Data']
		# get data and convert to rounded integer
		pos = temperature.index(' ')
		temperature = temperature[:pos]
		tf = round(float(temperature))
		return str(tf)
	except Exception:
		pass
	return '-'
		
def write_temperature(inkyphat):
	# get sensor data (top line)
	temperature = get_sensor_data(TEMP_SENSOR_1)
	time_font = ImageFont.truetype(inkyphat.fonts.PressStart2P, 25)
	w, h = time_font.getsize(temperature)
	inkyphat.text((inkyphat.WIDTH / 2 + 4, 5), temperature + '°', inkyphat.BLACK, time_font)	
	# write a 'v' indicating west sensor
	message = 'V'
	message_font = ImageFont.truetype(inkyphat.fonts.PressStart2P, 14)
	wm, hm = message_font.getsize(message)
	inkyphat.text((inkyphat.WIDTH - wm, 5), message, inkyphat.RED, message_font)
	# get sensor data (second line)
	temperature = get_sensor_data(TEMP_SENSOR_2)
	inkyphat.text((inkyphat.WIDTH / 2 + 4, h + 20), temperature + '°', inkyphat.BLACK, time_font)
	# write 'n' for north sensor
	message = 'N'
	wm, hm = message_font.getsize(message)
	inkyphat.text((inkyphat.WIDTH - wm, h + 20), message, inkyphat.RED, message_font)
	return

def write_weather_forecast(inkyphat):
	global weather_forecast_counter
	global weather_forecasts
	if weather_forecast_counter > 14:
		weather_forecast_counter = 0
		# get data from Yr
		# Paste link and append /varsel.xml
		r = requests.get('https://www.yr.no/nb/oversikt/dag/2-6296790/Sverige/V%C3%A4stra%20G%C3%B6taland/H%C3%A4rryda%20Kommun/Landvetter%20lufthavn/varsel.xml', timeout=10)
		mydoc = minidom.parseString(r.text)
		temperatures = mydoc.getElementsByTagName('temperature')
		precipitations = mydoc.getElementsByTagName('precipitation')	

		for i in range(3):
			t = str(temperatures[i].attributes['value'].value) + '° '
			if (precipitations[i].hasAttribute('minvalue')):
				minv = precipitations[i].attributes['minvalue'].value
				maxv = precipitations[i].attributes['maxvalue'].value
				t += str(maxv)
			else:
				t += '0'
			weather_forecasts[i] = t

	forecast_font = ImageFont.truetype(inkyphat.fonts.PressStart2P, 14)
	for i in range(3):
		inkyphat.text((0, i * inkyphat.HEIGHT / 3 + 10), weather_forecasts[i], inkyphat.BLACK, forecast_font)
		
	weather_forecast_counter += 1
	return

# start main loop, will never end...
while True:
	try:
		# write up some graphics
		inkyphat.line([(inkyphat.WIDTH / 2, 0), (inkyphat.WIDTH / 2, inkyphat.HEIGHT)], width=2, fill=inkyphat.RED)
		inkyphat.line([(inkyphat.WIDTH / 2, 79), (inkyphat.WIDTH, 79)], width=2, fill=inkyphat.RED)
		# write up data
		write_time(inkyphat)
		write_temperature(inkyphat)
		write_weather_forecast(inkyphat)
		# draw screen
		inkyphat.show()
		# wait one minute
		time.sleep(60)
		# clear screen
		inkyphat.clear()
	except Exception:
		pass
