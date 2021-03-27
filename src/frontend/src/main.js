import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts';

import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

createApp(App).use(router, VueApexCharts).mount('#app')