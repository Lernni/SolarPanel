import { defineStore } from 'pinia'
import { useSocketIO } from '../modules/useSocketIO'

const socket = useSocketIO()

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    data: {
      battery: {
        value: 0,
        soc: 0.0,
        capacity: 0.0,
        gain: {
          max: 0.0,
          min: 0.0,
          value: 0.0,
        },
      },
      voltage: {
        value: 0.0,
        min: {
          value: 0.0,
          date: '',
        },
        max: {
          value: 1.0,
          date: '',
        },
        avg: {
          yesterday: 0.0,
          lastWeek: 0.0,
        },
      },
      inputPower: 0.0,
      input_current: {
        value: 0.0,
        min: {
          value: 0.0,
          date: '',
        },
        max: {
          value: 1.0,
          date: '',
        },
        avg: {
          yesterday: 0.0,
          lastWeek: 0.0,
        },
      },
      outputPower: 0.0,
      output_current: {
        value: 0.0,
        min: {
          value: 0.0,
          date: '',
        },
        max: {
          value: 1.0,
          date: '',
        },
        avg: {
          yesterday: 0.0,
          lastWeek: 0.0,
        },
      },
    },
    ui: {
      detailsOpen: {},
    },
  }),

  actions: {
    update() {
      socket.emit('dashboard:getUpdate', (response) => {
        // set state from request response
        this.data.voltage.value = response.data.voltage
        this.data.input_current.value = response.data.input_current
        this.data.output_current.value = response.data.output_current
        this.data.battery.soc = response.data.soc
        this.data.battery.capacity = response.data.capacity

        // set computed state values
        this.data.battery.value = Math.round((response.data.soc / response.data.capacity) * 100)
        this.data.battery.gain.value =
          (this.data.input_current.value - this.data.output_current.value) / 3600
        this.data.inputPower = Number(
          this.data.voltage.value * this.data.input_current.value
        ).toFixed(1)
        this.data.outputPower = Number(
          this.data.voltage.value * this.data.output_current.value
        ).toFixed(1)

        // update min and max values if necessary
        if (this.data.voltage.value > this.data.voltage.max.value) {
          this.data.voltage.max.value = this.data.voltage.value
          this.data.voltage.max.date = response.data.timestamp
        }

        if (this.data.voltage.value < this.data.voltage.min.value) {
          this.data.voltage.min.value = this.data.voltage.value
          this.data.voltage.min.date = response.data.timestamp
        }

        if (this.data.input_current.value > this.data.input_current.max.value) {
          this.data.input_current.max.value = this.data.input_current.value
          this.data.input_current.max.date = response.data.timestamp
        }

        if (this.data.output_current.value > this.data.output_current.max.value) {
          this.data.output_current.max.value = this.data.output_current.value
          this.data.output_current.max.date = response.data.timestamp
        }
      })
    },

    detailedUpdate(metric) {
      socket.emit('dashboard:getDetailedUpdate', metric, (response) => {
        switch (metric) {
          case 'voltage':
            this.data.voltage.min.value = response.data.details.min
            this.data.voltage.min.date = response.data.details.min_date
            this.data.voltage.max.value = response.data.details.max
            this.data.voltage.max.date = response.data.details.max_date
            this.data.voltage.avg.yesterday = response.data.details.avg_yesterday
            this.data.voltage.avg.lastWeek = response.data.details.avg_week
            break

          case 'input_current':
            this.data.input_current.max.value = response.data.details.max
            this.data.input_current.max.date = response.data.details.max_date
            this.data.input_current.avg.yesterday = response.data.details.avg_yesterday
            this.data.input_current.avg.lastWeek = response.data.details.avg_week
            break

          case 'output_current':
            this.data.output_current.max.value = response.data.details.max
            this.data.output_current.max.date = response.data.details.max_date
            this.data.output_current.avg.yesterday = response.data.details.avg_yesterday
            this.data.output_current.avg.lastWeek = response.data.details.avg_week
            break

          case 'battery':
            this.data.battery.gain.min = response.data.details.max_soc_loss
            this.data.battery.gain.max = response.data.details.max_soc_gain
        }
      })
    },
  },
})
