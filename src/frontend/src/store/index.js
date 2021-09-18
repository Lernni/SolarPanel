import Vue from 'vue'
import Vuex from 'vuex'
import $socket from '../scripts/socketInstance'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    device: '',
    token: localStorage.getItem('token') || '',
  },

  actions: {
    login({commit}, credentials) {
      return new Promise((resolve, reject) => {
        $socket.emit("loginRequest", credentials, (response) => {
          console.log("response: " + response)
          if (response.success) {
            localStorage.setItem('token', response.token)
            $socket.auth.token = response.token
            commit('setToken', response.token)
            resolve(response)
          } else {
            localStorage.removeItem('token')
            reject()
          }
        })
      })
    },

    logout({commit}) {

      // eslint-disable-next-line no-unused-vars
      return new Promise((resolve, reject) => {
        localStorage.removeItem('token')
        commit('setToken', '')
        $socket.auth.token = ''
        resolve()
      })
    }
  },

  mutations: {
    setToken(state, token) {
      state.token = token
    },

    SOCKET_DEVICE_DEFINITION(state, data) {
      state.device = data.device
    },
  },

  getters: {
    isLoggedIn: state => (!!state.token || (state.device == "Internal")),
  }
})