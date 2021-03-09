# Webserver
## Vue CLI
>Existiert das Vue Projekt bereits, dann mit git clonen und die dependencies mittels `npm install` nachträglich hinzufügen
1. Befehle ausführen:
```
curl -sL https://deb.nodesource.com/setup_15.x | sudo -E bash -
sudo apt-get install -y nodejs
npx @vue/cli create webserver
```
Manuelle Installation auswählen und `vue-router` aktivieren

2. Bootstrap installieren:
```
cd webserver
npm i bootstrap jquery popper.js
```
3. Boostrap zu `src/main.js` hinzufügen:
```
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
```
>siehe https://travishorn.com/adding-bootstrap-to-a-vue-cli-project-98c2a30e0ed0
4. Development Server starten:
```
npm run serve
```
