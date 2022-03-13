# Erstkonfiguration Raspberry Pi
## Installieren von Raspberry Pi OS auf einem USB Flash Drive

> Eine einfache Installation direkt auf den USB Flash Drive ist zurzeit noch nicht möglich (siehe https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/bootflow_2711.md)

>Anleitung: https://www.tomshardware.com/how-to/boot-raspberry-pi-4-usb

>Achtung: Die SD-Karte sollte mindestens genauso groß sein, wie das USB Flash Drive, ansonsten wird dem Flash Drive weniger Speicher zugewiesen, als eigentlich zur Verfügung steht. In dem Fall sollte die Partition manuell vergrößert werden (siehe https://www.yourhelpcenter.de/2017/08/raspberry-pi-eine-partition-erweitern/ ; Bei der Meldung 'partition #2 contains a ext4 signature. Want to remove it?' 'Yes' auswählen)

1. Raspberry Pi OS Lite (32 Bit) auf eine SD Karte über Raspberry Pi Imager schreiben
2. Auf dem Datenträger die Datei `ssh` erstellen, um SSH zu aktivieren
3. `sudo raspi-config` aufrufen und Hostname ändern (System Options > Hostname) + Neustart
4. Folgende Befehle ausführen:
```
sudo apt update
sudo apt full-upgrade
sudo rpi-update
sudo reboot
sudo rpi-eeprom-update -d -a
```
>Falls der letzte Befehl ein Update durchführt, danach neustarten. Wahrscheinlich überflüssiger Befehl, da schon mit in den vorherigen Befehlen inbegriffen.
5. `sudo raspi-config` aufrufen: 
* Advanced Options > Bootloader Version > Latest > Reset boot ROM to defaults? > No
* Advanced Options > Boot Order > USB
* Finish > Reboot? > No
6. Raspi herunterfahren
7. SD Karte auf USB Flash Drive klonen (mit balenaEtcher)
8. Raspi nur mit USB Flash Drive starten

## Einrichten des Raspberry Pi
>Anleitung: https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/4

1. `sudo raspi-config` aufrufen:
* Localisation Options > Locale > de_DE.UTF-8 UTF-8 > None
* Localisation Options > Timezone > Europe > Berlin
* System Options > Password
>Locales 'None': https://raspberrypi.stackexchange.com/questions/1132/which-locale-should-i-select-during-the-raspbian-setup
2. Neuen Nutzer anlegen und dessen SSH-Passwort ändern:
>Anleitung: https://www.pcwelt.de/a/so-machen-sie-den-raspberry-pi-sicherer,3449552
```
sudo useradd -m [benutzer] -G sudo
sudo passwd [benutzer]
```
3. Nutzer 'pi' deaktivieren:
```
sudo passwd --lock pi
```
4. Anmeldung über SSH als 'root' unterbinden (`#PermitRootLogin no`) und Port ändern
```
sudo nano /etc/ssh/sshd_config
```
5. SSH-Dienst neustarten:
```
sudo /etc/init.d/ssh restart
```
6. `ssh-keygen` auf PC ausführen, der auf den Raspi per SSH zugreifen soll. (Alles mit Enter bestätigen, die Schlüssel befinden sich dann im Ordner '.ssh')
7. Den Ordner 'home/[benutzer]/.ssh' und darin die Datei `authorized_keys` anlegen:
```
mkdir .ssh
cd .ssh
touch authorized_keys
```
8. Die Datei `id_rsa.pub` mittels scp ins 'home/[benutzer]/.ssh' Verzeichnis kopieren
9. Den Inhalt der Datei an `authorized_keys` anhängen:
```
cat id_rsa.pub >> authorized_keys
```
10. `id_rsa.pub` entfernen
11. SSH-Dienst neustarten:
```
sudo /etc/init.d/ssh restart
```
12. VSCode Extension 'Remote - SSH' installieren und Verbindung dauerhaft hinzufügen
13. I2C für Non-Root User einrichten
```
sudo groupadd i2c
sudo chown :i2c /dev/i2c-1
sudo chmod g+rw /dev/i2c-1
sudo usermod -aG i2c [benutzer]
```
>siehe https://lexruee.ch/setting-i2c-permissions-for-non-root-users.html (Schritte 1-5)
14. `src/local_client/start_solarpanel.sh` an die Datei `/etc/rc.local` anhängen:

```
/home/[benutzer]/SolarPanel/src/local_client/start_solarpanel.sh 2>&1 | tee /home/[benutzer]/startup.log
```
15. Logindaten in die Datei `/solarpanel_data/config/login_credentials.json` schreiben:
```json
{
    "username": "[username]",
    "password": "[password]",
    "token": "[token]"
}
```

## Pakete installieren
1. Git:
```
sudo apt install git
git config --global user.name "Lernni"
git config --global user.email "Lernni@users.noreply.github.com"
git clone https://github.com/Lernni/SolarPanel.git
```
2. Docker:
```
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker lernni
sudo apt-get install python3-pip
sudo pip3 install docker-compose
```
3. fail2ban:
```
sudo apt-get install fail2ban
cd /etc/fail2ban
sudo cp jail.conf jail.local
sudo nano jail.local
```

>Unter '[sshd]' Änderungen vornehmen, wie siehe https://pimylifeup.com/raspberry-pi-fail2ban/ , Schritt 9 

```
sudo service fail2ban restart
```
4. I2C:
```
sudo apt-get install -y python-smbus
sudo apt-get install -y i2c-tools
```
- I2C-Interface manuell in `raspi-config` aktivieren

5. vnStat:
```
cd ~
git clone https://github.com/vergoh/vnstat-docker.git
docker build -t vergoh/vnstat .
docker run -d \
    --restart=unless-stopped \
    --network=host \
    -e HTTP_PORT=8685 \
    -v /etc/localtime:/etc/localtime:ro \
    -v /etc/timezone:/etc/timezone:ro \
    --name vnstat \
    vergoh/vnstat
```

## RTC einrichten
> siehe https://www.raspberry-pi-geek.de/ausgaben/rpg/2015/03/echtzeituhr-modul-ds3231-sorgt-fuer-genaue-zeitangaben
1. Folgende Zeile in `/etc/modules` einfügen:

```
i2c-bcm2708
```

## Display einrichten
1. Folgende Befehle ausführen:
```
cd ~
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
```
>siehe http://www.lcdwiki.com/4inch_HDMI_Display-C
2. `sudo reboot` aus `MPI4008-show` und `system_backup.sh` entfernen
3. `./MPI4008-show` auführen
4. `/boot/cmdline.txt` ersetzen mit:
```
console=serial0,115200 console=tty1 root=PARTUUID=592acc1f-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait fbcon=map:10 fbcon=font:ProFont6x11
```
>Hinweis: Spezifische `PARTUUID` aus der `cmdline.txt` des Systems verwenden

>siehe https://github.com/goodtft/LCD-show/issues/276
5. `sudo reboot` ausführen
6. Folgende Befehle ausführen:
```
sudo apt-get install --no-install-recommends xinit
sudo apt install xserver-xorg-video-fbdev
sudo apt-get install -y chromium-browser matchbox
```
>Vielleicht auch in `sudo raspi-config` eine bestimmte Displayauflösung auswählen, statt Standardauflösung
7. Schriftart 'Segoe UI' installieren:
```
cd /usr/share/fonts/truetype
sudo mkdir segoe
cd segoe
sudo wget -O segoe_ui.zip "https://drive.google.com/u/0/uc?id=1X6u8o0z6APX1RDn6ZaQwYZUeWsmnY21X&export=download"
sudo unzip segoe_ui.zip
sudo rm segoe_ui.zip
fc-cache
fc-list
```
>siehe https://www.fontmirror.com/segoe-ui
8. `nano start_browser.sh` erstellen mit:
```
#!/bin/sh
xset -dpms # disable DPMS (Energy Star) features.
xset s off # disable screen saver
xset s noblank # don't blank the video device
matchbox-window-manager &
chromium-browser --no-pings --incognito --noerrdialogs --disable-infobars --no-sandbox --kiosk $1
```
>Alle Chromium Commandline-Options: https://peter.sh/experiments/chromium-command-line-switches/
9. Skript ausführbar machen: `sudo chmod +x start_browser.sh`
10. In `/etc/X11/xinit/xserverrc` die Option `-nocursor` anfügen
11. Skript starten: `sudo startx ./start_browser.sh http://localhost:8080`