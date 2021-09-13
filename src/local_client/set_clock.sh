#!/bin/sh

# If connected to the Internet
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
    echo "\033[1;32mconnected to the internet...\033[0m"
    echo "set system and RTC time from NTP time server"
    # cannot set timezone to local time MEZ because of switching timezones (summer and winter time)
    # instead set timezone to UTC
    sudo timedatectl set-timezone UTC

    # set system clock from NTP Server
    sudo timedatectl set-ntp true &
    sleep 1
    timedatectl

    sudo timedatectl set-ntp false &
    sleep 1

    # get current datetime + 1 hour (MEZ)
    localtime=$(TZ=UTC date -d "+ 1 hour" "+%Y-%m-%d %H:%M:%S")
    echo "\033[1;32mcurrent datetime + 1 hour (MEZ): $localtime \033[0m"
    
    # set system clock and RTC to current datetime + 1 hour (MEZ)
    sudo timedatectl set-time "$localtime" &
    sleep 1
else
    echo "\033[0;31mno internet connection...\033[0m"
    echo "set system clock from RTC"

    timedatectl
    
    # Set system clock from RTC
    sudo hwclock -w
    sleep 1
fi

timedatectl