import { ref, computed } from 'vue'

import { defineStore } from 'pinia'
import { useSocketIO } from '../modules/useSocketIO'
import { useUnits } from '../modules/useUnits'

import moment from 'moment-timezone'

const socket = useSocketIO()
const units = useUnits()

export const useBrowserStore = defineStore('browser', () => {
  // state
  const range = ref({
    start: moment.utc().add(1, 'h').subtract(1, 'd').set({ seconds: 0, milliseconds: 0 }),
    end: moment.utc().add(1, 'h').set({ seconds: 0, milliseconds: 0 }),
  })

  const selectedUnits = ref(units.map((unit) => unit.value))

  // const graphValues

  // actions
  const fetchData = (callback) => {
    socket.emit(
      'browser:fetchData',
      {
        start_time: range.value.start.format('YYYY-MM-DD_HH-mm'),
        end_time: range.value.end.format('YYYY-MM-DD_HH-mm'),
        units: selectedUnits.value,
      },
      (response) => {
        callback(response.data)
      }
    )
  }

  // getters/setters
  const startTime = computed({
    get() {
      return range.value.start.toDate()
    },
    set(newValue) {
      range.value.start = moment.utc(newValue)
    },
  })

  const endTime = computed({
    get() {
      return range.value.end.toDate()
    },
    set(newValue) {
      range.value.end = moment.utc(newValue)
    },
  })

  const timeRange = computed({
    get() {
      return {
        start: startTime.value,
        end: endTime.value,
      }
    },
    set({ start, end }) {
      startTime.value = start
      endTime.value = end
    },
  })

  return { range, selectedUnits, fetchData, startTime, endTime, timeRange }
})
