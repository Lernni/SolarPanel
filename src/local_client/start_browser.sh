#!/bin/sh
xset -dpms # disable DPMS (Energy Star) features.
xset s off # disable screen saver
xset s noblank # don't blank the video device
matchbox-window-manager &
chromium-browser --disk-cache-dir=/dev/null --disk-cache-size=1 --no-pings --incognito --noerrdialogs --disable-infobars --no-sandbox --kiosk $1
