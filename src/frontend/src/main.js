import { createApp } from 'vue'
import './tailwind.css'
import App from './App.vue'
import { routes } from './routes.js'
import { createRouter, createWebHistory } from 'vue-router'
import HighchartsVue from 'highcharts-vue'
import MathJax, { initMathJax, renderByMathjax } from 'mathjax-vue3'
import { createPinia } from 'pinia'

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
app.use(HighchartsVue)
app.use(MathJax)
app.use(createPinia())
app.mount('#app')
