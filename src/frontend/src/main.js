import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts';

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'apexcharts';

createApp(App).component('apexchart', VueApexCharts)
createApp(App).use(router).use(VueApexCharts).mount('#app')
