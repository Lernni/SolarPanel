import Vue from 'vue'
import Vuex from 'vuex'
import $socket from '../scripts/socketInstance'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    device: '',
    token: localStorage.getItem('token') || '',
    records: {
      voltage: [],
      input_current: [],
      output_current: [],
      power: [],
    },
    entities: [],
    settings: {
      // recording: true,
      // input_shunt: 0.00001,
      // output_shunt: 0.0031,
    }
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
    
    SOCKET_SPARKLINE_RECORDS(state, data) {
      state.records = data
      state.records.power = []
      for (let i = 0; i < state.records.voltage.length; i++) {
        state.records.power[i] = state.records.voltage[i] * state.records.input_current[i]
      }
    },

    SOCKET_SPARKLINE_UPDATE(state, data) {
      state.records.voltage = state.records.voltage.slice(1)
      state.records.voltage.push(data.voltage)

      state.records.input_current = state.records.input_current.slice(1)
      state.records.input_current.push(data.input_current)

      state.records.output_current = state.records.output_current.slice(1)
      state.records.output_current.push(data.output_current)

      state.records.power = state.records.power.slice(1)
      state.records.power.push(data.voltage * data.input_current)
    },

    SOCKET_DB_ENTITIES_SIMPLE(state, data) {
      state.entities = []

      for (let i = 0; i < data.length; i++) {
        state.entities.push({
          x: "records",
          y: [data[i][0] * 1000, data[i][1] * 1000],
        })
      }
    },

    SOCKET_SETTINGS_UPDATE(state, data) {
      state.settings = data
    }
  },

  getters: {
    isLoggedIn: state => (!!state.token || (state.device == "Internal")),
  }
})