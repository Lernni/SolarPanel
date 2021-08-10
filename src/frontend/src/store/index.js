import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    records: {
      voltage: [],
      input_current: [],
      output_current: [],
      power: [],
    }
  },

  mutations: {
    SOCKET_SPARKLINE_RECORDS(state, data) {
      state.records = data.records
    },
    SOCKET_SPARKLINE_UPDATE(state, data) {
      state.records.voltage = state.records.voltage.slice(1)
      state.records.voltage.push(data.voltage)

      state.records.input_current = state.records.input_current.slice(1)
      state.records.input_current.push(data.input_current)

      state.records.output_current = state.records.output_current.slice(1)
      state.records.output_current.push(data.output_current)
    }
  },

})