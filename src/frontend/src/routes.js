import Dashboard from './views/Dashboard.vue'
import Browser from './views/Browser.vue'
import Settings from './views/Settings.vue'
import NotFound from './views/NotFound.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
  {
    path: '/',
    component: Dashboard,
    meta: { title: 'Dashboard', icon: 'SunIcon', showItem: true },
  },
  {
    path: '/browser',
    component: Browser,
    meta: { title: 'Browser', icon: 'ChartBarIcon', showItem: true },
  },
  {
    path: '/settings',
    component: Settings,
    meta: { title: 'Einstellungen', icon: 'AdjustmentsIcon', showItem: true },
  },
  {
    path: '/:path(.*)',
    component: NotFound,
    meta: { title: 'NotFound', showItem: false },
  },
]
