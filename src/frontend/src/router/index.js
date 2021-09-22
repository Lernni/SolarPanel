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
import Login from '../views/Login.vue'

import store from '../store'
import $socket from '../scripts/socketInstance'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/',
    name: 'dashboard',
    component: Dashboard,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/stats',
    name: 'records',
    component: Stats,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'browser',
        name: 'browser',
        component: Browser,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: 'export',
        name: 'export',
        component: Export,
        meta: {
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/system',
    name: 'system',
    component: System,
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'settings',
        name: 'settings',
        component: Settings,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: 'events',
        name: 'events',
        component: Events,
        meta: {
          requiresAuth: true
        }
      },
      {
        path: 'info',
        name: 'info',
        component: Info,
        meta: {
          requiresAuth: true
        }
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
  if (!to.meta.requiresAuth || store.getters.isLoggedIn) {
    $socket.emit('navigate', from.name, to.name)
    return next()
  }

  //return next('/login')
})

export default router
