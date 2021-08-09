import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Stats from '../views/Stats.vue'
import Browser from '../views/Stats/Browser.vue'
import Export from '../views/Stats/Export.vue'
import System from '../views/System.vue'
import Settings from '../views/System/Settings.vue'
import Events from '../views/System/Events.vue'
import Info from '../views/System/Info.vue'

import io from 'socket.io-client';

const socket = io()

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard
  },
  {
    path: '/stats',
    name: 'records',
    component: Stats,
    children: [
      {
        path: 'browser',
        name: 'browser',
        component: Browser
      },
      {
        path: 'export',
        name: 'export',
        component: Export
      }
    ]
  },
  {
    path: '/system',
    name: 'system',
    component: System,
    children: [
      {
        path: 'settings',
        name: 'settings',
        component: Settings
      },
      {
        path: 'events',
        name: 'events',
        component: Events
      },
      {
        path: 'info',
        name: 'info',
        component: Info
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// eslint-disable-next-line no-unused-vars
router.beforeEach((to, from, next) => {
  socket.emit('navigate', to.name)
})

export default router
