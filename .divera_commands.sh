#!/bin/bash

# This file is an extension for the bash which contains the commands for
# turning the screen ond and off and also starts and stops the monitor.
# Source this file in your bash.rc to have the commands in your terminal.

#The url of your monitor (with Acesskey for autologin).
MONITOR={YOUR MONITOR URL}

# This function starts or stops the divera monitor.
function monitor(){
	if [ $1 = on ]; then
		# starts chromium in in kiosk mode
		chromium-browser --noerrdialogs --kiosk --incognito $MONITOR &>/dev/null &
	elif [ $1 = off ]; then
		# just kill every chromium process
		pkill chromium >/dev/null
	else
		echo Unknown parameter
	fi
}

# Turns the screen on and off. Every screen is diffrent and many are bad programmed
# for that here are two diffrent ways for turning it on and off.
function screen(){
	if [ $1 = on ]; then
		# Version 1: enables hdmi port after the screen was in standby
		vcgencmd display_power 1 >/dev/null
		
		# Version 2: send cec-signal to the screen that he should wake up
		#echo on 0 | cec-client -s -d 1

		# Version 2b: if the screen turns on but at wrong input (e.g. AV1) force it to
		# switch to HDMI1 port. This works only if the screen is on already
		# therefore send it a few times in a row. 4F:82:10:00 is HDMI1, 4F:82:20:00
		# is HDMI2, 4F:82:30:00 is HDMI3 and so on. Attention this is an unoffical
		# cec-signal which may not work with your screen.
		#echo tx 4F:82:10:00 | cec-client -s -d 1
		#echo tx 4F:82:10:00 | cec-client -s -d 1
		#echo tx 4F:82:10:00 | cec-client -s -d 1
		#echo tx 4F:82:10:00 | cec-client -s -d 1
		#echo tx 4F:82:10:00 | cec-client -s -d 1
		#echo tx 4F:82:10:00 | cec-client -s -d 1
		#echo tx 4F:82:10:00 | cec-client -s -d 1
	elif [ $1 = off ]; then
		# Version 1: disable hdmi port that the screen goes in standby
		vcgencmd display_power 0 >/dev/null

		# Version 2: send cec-signal to the screen that he should go in standby
		#echo standby 0 | cec-client -s -d 1
	else
		echo Unknown parameter
	fi
}
