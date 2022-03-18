# Erstkonfiguration Raspberry Pi
## Installieren von Raspberry Pi OS

1. Raspberry Pi OS Lite (64 Bit) auf eine SD Karte über Raspberry Pi Imager schreiben
2. Auf dem Datenträger die Datei `ssh` erstellen, um SSH zu aktivieren
3. Raspberry Pi mit Datenträger starten
4. `sudo raspi-config` aufrufen und Hostname ändern (System Options > Hostname) + Neustart
5. Folgende Befehle ausführen:
```
sudo apt update
sudo apt full-upgrade
sudo reboot
```


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
sudo useradd -m [user] -G sudo
sudo passwd [user]
```
3. Nutzer 'pi' deaktivieren:
```
sudo passwd --lock pi
```
4. Anmeldung über SSH als 'root' unterbinden (`PermitRootLogin no`) und Port ändern (`Port [number]`)
```
sudo nano /etc/ssh/sshd_config
```
5. SSH-Dienst neustarten und Raspberry Pi neustarten:
```
sudo /etc/init.d/ssh restart
sudo reboot
```
6. `ssh-keygen` auf PC ausführen, der auf den Raspi per SSH zugreifen soll. (Alles mit Enter bestätigen, die Schlüssel befinden sich dann im Ordner '~/.ssh')
7. Auf dem Raspberry Pi das Verzeichnis '~/[user]/.ssh' anlegen und darin die Datei `authorized_keys` erstellen:
```
cd ~
mkdir .ssh
cd .ssh
touch authorized_keys
```
8. Auf dem PC Die Datei `id_rsa.pub` mittels scp ins '~/[user]/.ssh' Verzeichnis auf den Raspberry kopieren
```
scp -P [port] ~/.ssh/id_rsa.pub [user]@[hostname]:~/.ssh/
```
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
1. **Git**
```
sudo apt install git
git config --global user.name "Lernni"
git config --global user.email "Lernni@users.noreply.github.com"
cd ~
git clone https://github.com/Lernni/SolarPanel.git
```
2. **Docker**
```
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker ${USER}
sudo apt-get install python3-pip
sudo pip3 install docker-compose
docker-compose --version
```
3. **fail2ban**
```
sudo apt install fail2ban
cd /etc/fail2ban
sudo cp jail.conf jail.local
sudo nano jail.local
```

4. Unter Abschnitt '[sshd]' Änderungen vornehmen, wie siehe https://pimylifeup.com/raspberry-pi-fail2ban/ (Schritt 9):

```
[sshd]
port    = [ssh_port_number]
logpath = %(sshd_log)s
backend = %(sshd_backend)s
enabled = true
filter = sshd
bantime = 600
maxretry = 3
```

5. Fail2Ban Service neustarten

```
sudo service fail2ban restart
```
6. **I2C**
```
sudo apt install -y python3-smbus i2c-tools
```
7. I2C-Interface manuell in `raspi-config` aktivieren (Interface Options > I2C > Yes)

8. I2C für Non-Root User einrichten
```
sudo groupadd i2c
sudo chown :i2c /dev/i2c-1
sudo chmod g+rw /dev/i2c-1
sudo usermod -aG i2c ${USER}
```
>siehe https://lexruee.ch/setting-i2c-permissions-for-non-root-users.html (Schritte 1-5)

9. **vnStat**
```
cd ~
git clone https://github.com/vergoh/vnstat-docker.git
sudo chmod 666 /var/run/docker.sock
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

10. **ngrok**
```
cd ~
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm64.zip
unzip ngrok-stable-linux-arm64.zip
./ngrok --version
sudo rm ngrok-stable-linux-arm64.zip
./ngrok authtoken [auth token]
```


## RTC einrichten
> siehe https://www.raspberry-pi-geek.de/ausgaben/rpg/2015/03/echtzeituhr-modul-ds3231-sorgt-fuer-genaue-zeitangaben
1. Folgende Zeile in `/etc/modules` einfügen:

```
i2c-bcm2708
```
## Grafiktreiber
1. Folgende Befehle ausführen:
```
cd ~
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
```
>siehe http://www.lcdwiki.com/4inch_HDMI_Display-C
2. `./MPI4008-show` auführen
3. `sudo reboot` ausführen


<details closed>
<summary>Alternative Installation auf USB-Flash-Drive</summary>

2. `sudo reboot` aus `MPI4008-show` und `system_backup.sh` entfernen
3. `./MPI4008-show` auführen
4. `/boot/cmdline.txt` ersetzen mit:
```
console=serial0,115200 console=tty1 root=PARTUUID=592acc1f-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait fbcon=map:10 fbcon=font:ProFont6x11
```
>Hinweis: Spezifische `PARTUUID` aus der `cmdline.txt` des Systems verwenden

>siehe https://github.com/goodtft/LCD-show/issues/276
5. `sudo reboot` ausführen

</details>

## Anzeige einrichten

1. Folgende Befehle ausführen:
```
sudo apt install -y --no-install-recommends xinit
sudo apt install -y xserver-xorg-video-fbdev chromium-browser matchbox
sudo mv /usr/share/X11/xorg.conf.d/99-fbturbo.conf ~
sudo ln -s /usr/lib/chromium-browser/swiftshader/libGLESv2.so /usr/lib/chromium-browser/
sudo ln -s /usr/lib/chromium-browser/swiftshader/libEGL.so /usr/lib/chromium-browser/
```
>Vielleicht auch in `sudo raspi-config` eine bestimmte Displayauflösung auswählen, statt Standardauflösung
2. Schriftart 'Segoe UI' installieren:
```
cd /usr/share/fonts/truetype
sudo mkdir segoe
cd segoe
sudo wget -O segoe_ui.zip "https://drive.google.com/u/0/uc?id=1X6u8o0z6APX1RDn6ZaQwYZUeWsmnY21X&export=download"
sudo unzip segoe_ui.zip
sudo rm segoe_ui.zip
fc-cache
fc-list
cd ~
```
>siehe https://www.fontmirror.com/segoe-ui

3. In `/etc/X11/xinit/xserverrc` die Option `-nocursor` anfügen


## SolarPanel einrichten
1. Aktuelle Version herunterladen
```
cd ~/SolarPanel
git pull
```

2. `src/local_client/start_solarpanel.sh` an die Datei `/etc/rc.local` anhängen:

```
/home/[user]/SolarPanel/src/local_client/start_solarpanel.sh 2>&1 | tee /home/[user]/startup.log
```
3. Logindaten in die Datei `/solarpanel_data/config/login_credentials.json` schreiben:
```json
{
    "username": "[username]",
    "password": "[password]",
    "token": "[token]"
}
```