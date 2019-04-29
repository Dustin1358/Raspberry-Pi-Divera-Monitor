#!/usr/bin/env python3

import subprocess
import datetime
import requests
import time
import RPi.GPIO as GPIO


ACCESSKEY="{YOUR ACCESS KEY}"
API_URL="https://www.divera247.com/api/last-alarm?accesskey="+ACCESSKEY
SENSOR_PIN = 23
SCREEN_ACTIVE=True
SCREENSAVER_ACTIVE=False
DUTY_TIME=False
ALARM_ACTIVE =False

#wrapper function that calls the divera monitor commands from the bash script
def monitor(command):
	if(command=="on"):
		subprocess.Popen(['bash','-c','. .divera_commands.sh; monitor on'])
	elif(command=="off"):
		subprocess.Popen(['bash','-c','. .divera_commands.sh; monitor off'])

#wrapper function that calls the diver screen commands from the bash script
def screen(command):
	global SCREEN_ACTIVE
	if(command=="on"):
		print("Turns screen on")
		if(ALARM_ACTIVE):
			screen_saver("off")
		else:
			init_screen_saver()
		SCREEN_ACTIVE=True
		subprocess.Popen(['bash','-c','. .divera_commands.sh; screen on']).wait()
	elif(command=="off"):
		print("Turns screen off")
		screen_saver("off")
		SCREEN_ACTIVE=False
		subprocess.Popen(['bash','-c','. .divera_commands.sh; screen off']).wait()

#wrapper function that turns the screensaver on/off
def screen_saver(command):
	global SCREENSAVER_ACTIVE
	if(command=="on"):
		print("Turns screensaver on")
		SCREENSAVER_ACTIVE=True
		subprocess.Popen(['xscreensaver-command', '-activate']).wait()
	elif(command=="off"):
		print("Turns screensaver off")
		SCREENSAVER_ACTIVE=False
		subprocess.Popen(['xscreensaver-command', '-deactivate']).wait()

#callback function which handels the reconized motion
def motion_detected(channel):
	if(GPIO.input(channel)):#motion detected
		print('Motion detected!')
		if(SCREEN_ACTIVE and SCREENSAVER_ACTIVE):
			print("Turn screensaver off")
			screen_saver("off")
		elif(not SCREEN_ACTIVE):
			print("Turns screen on")
			screen("on")
	else:#no motion
		print('No motion anymore!')
		if(DUTY_TIME and not ALARM_ACTIVE):
			screen_saver("on")
		elif(not DUTY_TIME and not ALARM_ACTIVE):
			screen("off")

#turns screensaver on/off depending on the motion detection
def init_screen_saver():
	if(GPIO.input(SENSOR_PIN)):
		screen_saver("off")
	else:
		screen_saver("on")
	
#at boot show the monitor
monitor("on")

#initializes GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_PIN, GPIO.IN)

#set callback
GPIO.add_event_detect(SENSOR_PIN , GPIO.BOTH, callback=motion_detected)

#initializes screensaver depending on motion detector
init_screen_saver()

 
while True:

	#sets the alarm except for the test alarm ("Probealarm")
	try:
		result = requests.get(API_URL).content.decode()
		ALARM_ACTIVE = "true" in result and "success" in result and "Probealarm" not in result
	except: #if not internet connection avaible show
		#screen that people recognize that somethong is wrong
		ALARM_ACTIVE=True


	now=datetime.datetime.now()

	day_of_week=now.weekday()+1 #1=Montag
	hour=now.hour
	minutes=now.minute


	#here you can define your duty times
	#Wednesday duty
	if(day_of_week==3 and hour >= 17):
		DUTY_TIME=True
	elif(day_of_week==4 and hour < 1):
		DUTY_TIME=True
	#Saturday duty
	elif(day_of_week== 6 and hour >= 7 and hour <= 19):
		DUTY_TIME=True
	else:
		DUTY_TIME=False


	#first all cases where the screen is not active
	if(SCREEN_ACTIVE == False):
		#case: active mission or duty time
		if(ALARM_ACTIVE == True or DUTY_TIME == True):
			print("Turning display on")
			screen("on")
		#case: monitor off an no mission and it is night time so make updates
		elif(ALARM_ACTIVE == False and hour == 3 and minutes == 5):
			print("Updating and restarting Raspberry")
			#wait a moment that he wont do two updates when he is faster then a minute with update and reboot
			time.sleep(45)
			subprocess.Popen(['sudo', 'apt', 'update']).wait()
			subprocess.Popen(['sudo', 'apt', '--yes', '--force-yes', 'upgrade']).wait()
			subprocess.Popen(['sudo', 'reboot'])
	#cases where the screen is active
	else:
		#case: no mission and no standby but monitor on
		if(ALARM_ACTIVE == False and DUTY_TIME == False and SCREENSAVER_ACTIVE):
			print("Turn display of")
			screen("off")


	#sleeps 30 seconds and starts again
	time.sleep(30)
