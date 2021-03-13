import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Stats from '../views/Stats/Stats.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    icon: 'dashboard'
  },
  {
    path: '/stats',
    name: 'Messwerte',
    component: Stats,
    icon: 'stats'
  },
  {
    path: '/settings',
    name: 'Einstellungen',
    component: Settings,
    icon: 'settings'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
