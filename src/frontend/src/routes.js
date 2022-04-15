import Dashboard from './views/Dashboard.vue'
import Browser from './views/Browser.vue'
import Settings from './views/Settings.vue'
import NotFound from './views/NotFound.vue'

/** @type {import('vue-router').RouterOptions['routes']} */
export const routes = [
  { path: '/', component: Dashboard, meta: { title: 'Dashboard' } },
  { path: '/browser', component: Browser, meta: { title: 'Browser' } },
  { path: '/settings', component: Settings, meta: { title: 'Settings' } },

  { path: '/:path(.*)', component: NotFound },
]
