import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import VueApexCharts from 'vue-apexcharts'
import VueSocketIO from 'vue-socket.io'
import Vuelidate from 'vuelidate'
import VueKatex from 'vue-katex';
import VueScreen from 'vue-screen';
import $socket from './scripts/socketInstance'

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'katex/dist/katex.min.css';

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.use(VueApexCharts)
Vue.use(Vuelidate)
Vue.use(VueKatex)
Vue.use(VueScreen, 'bootstrap')

Vue.use(new VueSocketIO({
  debug: true,
  connection: $socket,
  vuex: {
    store,
    actionPrefix: 'SOCKET_',
    mutationPrefix: 'SOCKET_',
  },
}))

Vue.config.productionTip = false
Vue.component('apexchart', VueApexCharts)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
