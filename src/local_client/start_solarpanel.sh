#!/bin/sh

echo "(1/6) - set system time..."

echo ds3231 0x68 | sudo tee /sys/class/i2c-adapter/i2c-1/new_device
/home/lernni/SolarPanel/src/local_client/set_clock.sh

echo "(2/6) - start traffic monitor vnstat..."
/bin/su -c "docker run -d --restart=unless-stopped --network=host -e HTTP_PORT=8685 -v /etc/localtime:/etc/localtime:ro -v /etc/timezone:/etc/timezone:ro --name vnstat vergoh/vnstat" - lernni

echo "(3/6) - update installed packages..."

apt update && apt full-upgrade -y

echo "(4/6) - init & start SolarPanel..."

# prepare named pipe
mkdir /home/lernni/solarpanel_data
mkfifo /home/lernni/solarpanel_data/host_cmd_interface
chown -R lernni /home/lernni/solarpanel_data
/home/lernni/SolarPanel/src/local_client/host_cmd_interface.sh &

# docker-compose needs to be started as user 'lernni', to be able to access the named pipe for host commands
/bin/su -c "docker-compose -f /home/lernni/SolarPanel/src/docker-compose.yml up -d" - lernni

echo "(5/6) - open ngrok tunnels..."
/home/lernni/ngrok start --config=/home/lernni/ngrok.yml --all > /dev/null &

echo "(6/6) - open browser window to localhost..."

startx /home/lernni/SolarPanel/src/local_client/start_browser.sh http://localhost &