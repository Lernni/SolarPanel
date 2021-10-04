#!/bin/sh

echo "(1/5) - set system time..."

echo ds3231 0x68 | sudo tee /sys/class/i2c-adapter/i2c-1/new_device
/home/lernni/SolarPanel/src/local_client/set_clock.sh

echo "(2/5) - update installed packages..."

apt update && apt full-upgrade -y

echo "(3/5) - init & start SolarPanel..."

# prepare named pipe
mkdir /home/lernni/solarpanel_data
mkfifo /home/lernni/solarpanel_data/host_cmd_interface
chown -R lernni /home/lernni/solarpanel_data
/home/lernni/SolarPanel/src/local_client/host_cmd_interface.sh &

# docker-compose needs to be started as user 'lernni', to be able to access the named pipe for host commands
/bin/su -c "docker-compose -f /home/lernni/SolarPanel/src/docker-compose.yml up -d" - lernni

echo "(4/5) - open ngrok tunnels..."
/home/lernni/ngrok start --config=/home/lernni/ngrok.yml --all > /dev/null &

echo "(5/5) - open browser window to localhost..."

startx /home/lernni/SolarPanel/src/local_client/start_browser.sh http://localhost &