#!/bin/sh

echo "(1/4) - set system time..."

echo ds3231 0x68 | sudo tee /sys/class/i2c-adapter/i2c-1/new_device
/home/lernni/SolarPanel/src/local_client/set_clock.sh

echo "(2/4) - update installed packages..."

sudo apt update && sudo apt full-upgrade -y

echo "(3/4) - start SolarPanel..."

docker-compose -f /home/lernni/SolarPanel/src/docker-compose.yml up -d

echo "(4/4) - open browser window to localhost..."

sudo startx /home/lernni/SolarPanel/src/local_client/start_browser.sh http://localhost &