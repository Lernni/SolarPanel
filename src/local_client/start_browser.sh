#!/bin/sh
matchbox-window-manager &
chromium-browser --disk-cache-dir=/dev/null --disk-cache-size=1 --no-pings --incognito --noerrdialogs --disable-infobars --no-sandbox --kiosk $1
