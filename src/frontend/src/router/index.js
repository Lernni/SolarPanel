import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Stats from '../views/Stats.vue'
import Browser from '../views/Stats/Browser.vue'
import Export from '../views/Stats/Export.vue'
import System from '../views/System.vue'
import Settings from '../views/System/Settings.vue'
import Events from '../views/System/Events.vue'
import Info from '../views/System/Info.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/stats',
    name: 'Messwerte',
    component: Stats,
    children: [
      {
        path: 'browser',
        name: 'Browser',
        component: Browser
      },
      {
        path: 'export',
        name: 'Export',
        component: Export
      }
    ]
  },
  {
    path: '/system',
    name: 'System',
    component: System,
    children: [
      {
        path: 'settings',
        name: 'Einstellungen',
        component: Settings
      },
      {
        path: 'events',
        name: 'Ereignisse',
        component: Events
      },
      {
        path: 'info',
        name: 'Systeminfo',
        component: Info
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: "active"
})

export default router
