#!/usr/bin/env python3

import subprocess
import datetime
import requests
import time

ACCESSKEY="{YOUR ACCESS KEY}"
API_URL="https://www.divera247.com/api/last-alarm?accesskey="+ACCESSKEY
screen_active=True

#wrapper methode that calls the diver monitor commands from the bash script
def monitor(command):
	if(command=="on"):
		subprocess.Popen(['bash','-c','. .divera_commands.sh; monitor on'])
	elif(command=="off"):
		subprocess.Popen(['bash','-c','. .divera_commands.sh; monitor off'])

#wrapper methode that calls the diver screen commands from the bash script
def screen(command):
	if(command=="on"):
		subprocess.Popen(['bash','-c','. .divera_commands.sh; screen on'])
	elif(command=="off"):
		subprocess.Popen(['bash','-c','. .divera_commands.sh; screen off'])

#at boot show the monitor
monitor("on")

while True:

	try:
		alarm_active = "false" not in requests.get(API_URL).content.decode()
	except: #if not internet connection avaible show
		#screen that people recognize that somethong is wrong 
		alarm_active=True
		
	now=datetime.datetime.now()
	
	day_of_week=now.weekday()+1 #1=Montag
	hour=now.hour
	minutes=now.minute
	duty_time=False
	
	#here you can define your duty times
	#Wednesday duty
	if(day_of_week==3 and hour >= 17):
		duty_time=True
	if(day_of_week==4 and hour < 1):
		duty_time=True
	#Saturday duty
	if(day_of_week== 6 and hour >= 7 and hour <= 19):
		duty_time=True

	#case: active mission and monitor off
	if(alarm_active == True and screen_active == False):
		print("Mission turning display on")
		screen("on")
		screen_active=True
        
	#case: duty time and mission off
	elif(duty_time == True and screen_active == False):
		print("Duty turning display on")
		screen("on")
		screen_active=True
        
	#case: no mission and no standby but monitor on
	elif(alarm_active == False and duty_time == False and screen_active == True):
		print("Turn display off")
		screen("off")
		screen_active=False
    
	#case: monitor off an no mission and it is night time so make updates
	elif(alarm_active == False and screen_active == False and hour == 3 and minutes == 5):
		print("Updating and restarting Raspberry")
		#wait a moment that he wont do two updates when he is faster then a minute with update and reboot
		time.sleep(45)
		subprocess.Popen(['sudo', 'apt', 'update']).wait()
		subprocess.Popen(['sudo', 'apt', '--yes', '--force-yes', 'upgrade']).wait()
		subprocess.Popen(['sudo', 'reboot'])
        
    #sleeps 30 seconds and starts again
	time.sleep(30)
