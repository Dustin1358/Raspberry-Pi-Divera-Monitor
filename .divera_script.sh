#!/bin/bash
 
ACCESSKEY="{YOUR ACCESS KEY}"
API_URL="https://www.divera247.com/api/last-alarm?accesskey=${ACCESSKEY}"
IS_MONITOR_ACTIVE=true

# includes the divera commands
source .divera_commands.sh

# at boot show the monitor
monitor on
 
while true; do
    HAS_ALARM=`curl -s ${API_URL} | jq -r -j '.success'`
    DOW=$(date +%u) #Monday=1 
    HOUR=$(date +%H)
    MINUTES=$(date +%M)
    DUTY_TIME=false

    # here you can define your duty times
    #Wednesday duty
    if [ $DOW = 3 ] && [ $HOUR -ge 17 ]; then
    	DUTY_TIME=true
    fi
    if [ $DOW = 4 ] && [ $HOUR -lt 1 ]; then
    	DUTY_TIME=true
    fi
    #saturday duty
    if [ $DOW = 6 ] && [ $HOUR -ge 7 ] && [ $HOUR -le 19 ]; then
    	DUTY_TIME=true
    fi
    
    
    #case: active mission and monitor off
    if [ $HAS_ALARM = true ] && [ $IS_MONITOR_ACTIVE = false ]; then
        echo "Mission turning display on"
        screen on
        IS_MONITOR_ACTIVE=true
        
    #case: duty time and mission off
    elif [ $DUTY_TIME = true ] && [ $IS_MONITOR_ACTIVE = false ]; then
        echo "Duty turning display on"
        screen on
        IS_MONITOR_ACTIVE=true
        
    #case: no mission and no duty time but monitor on
    elif [ $HAS_ALARM = false ] && [ $DUTY_TIME = false ] && [ $IS_MONITOR_ACTIVE = true ]; then
        echo "Turn display off"
        screen off
        IS_MONITOR_ACTIVE=false
    
    #case: monitor off and no mission and it is night time then make updates
    elif [ $HAS_ALARM = false ] && [ $IS_MONITOR_ACTIVE = false ] && [ $HOUR = 3 ] && [ $MINUTES = 5 ]; then
        echo "Updating and restarting Raspberry"

	#wait a moment that he wont do two updates when he is faster then a minute with update and reboot
        sleep 45

        sudo apt update
        sudo apt --yes --force-yes upgrade
        sudo reboot
    fi
    
    #sleeps 30 seconds and starts again
    sleep 30
done
