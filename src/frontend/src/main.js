import { createApp } from 'vue'
import './tailwind.css'
import App from './App.vue'
import { routes } from './routes.js'
import { createRouter, createWebHistory } from 'vue-router'
import VueApexCharts from 'vue3-apexcharts'
import MathJax, { initMathJax, renderByMathjax } from 'mathjax-vue3'

function onMathJaxReady() {
  const element = document.querySelector('#mathjax-render-element')
  renderByMathjax(element)
}

initMathJax({}, onMathJaxReady)

const app = createApp(App)

const router = createRouter({
  history: createWebHistory(),
  routes,
})

app.use(router)
app.use(VueApexCharts)
app.use(MathJax)
app.mount('#app')
