# Erstkonfiguration Raspberry Pi
## Installieren von Raspberry Pi OS auf einem USB Flash Drive

> Eine einfache Installation direkt auf den USB Flash Drive ist zurzeit noch nicht möglich (siehe https://www.raspberrypi.org/documentation/hardware/raspberrypi/bootmodes/bootflow_2711.md)

>Anleitung: https://www.tomshardware.com/how-to/boot-raspberry-pi-4-usb

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
4. Anmeldung über SSH als 'root' unterbinden: `#PermitRootLogin no`
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

## Pakete installieren
1. Docker installieren und testen:
```
curl -fsSL https://get.docker.com | sh
sudo docker run armhf/hello-world
```