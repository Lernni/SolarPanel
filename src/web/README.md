# Frontend
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
>siehe https://travishorn.com/adding-bootstrap-to-a-vue-cli-project-98c2a30e0ed0
3. ApexCharts installieren:
```
npm install --save apexcharts
npm install --save vue3-apexcharts
```
>siehe https://apexcharts.com/docs/vue-charts/
4. `main.js` anpassen
5. Development Server starten:
```
npm run serve
```

