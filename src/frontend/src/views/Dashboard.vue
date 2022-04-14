<template>
  <b-row>
    <b-col>
      <b-card-group deck>
        <ParameterCard parameter="Spannung" unit="V" :seriesData=records.voltage />
        <ParameterCard parameter="Eingangsstrom" unit="A" color="#E91E63" :seriesData=records.input_current />
        <ParameterCard parameter="Ausgangsstrom" unit="A" color="#E91E63" :seriesData=records.output_current />
        <ParameterCard v-if="device == 'Internal'" parameter="Ladezustand" unit="Ah" :seriesData=records.soc />
        <ParameterCard  v-if="device == 'External'" no_value parameter="Akkustatus" color="#00ebb9" :seriesData=records.soc>
          <div class="row battery-info no-gutters mb-2">
            <div class="col-5 col-lg-6 col-md-3">
              <Battery class="battery" :soc="battery.level" />
            </div>
            <div class="col-7 col-lg-6 col-md-9">
              <h5>Ladezustand</h5>
              <h2>{{battery.soc}} Ah</h2>
              <br>
              <h5>Kapazität</h5>
              <h2>{{battery.capacity}} Ah</h2>
            </div>
          </div>
        </ParameterCard>
      </b-card-group>
    </b-col>
    <b-col v-if="device == 'Internal'" class="col-3">
      <Battery class="battery" :soc="battery.level" />
    </b-col>
  </b-row>

</template>

<script>
import ParameterCard from '../components/ParameterCard.vue'
import Battery from '../components/Battery.vue'

export default {
  name: 'Dashboard',
  components: {
    ParameterCard,
    Battery
  },

  data() {
    return {
      records: {},
      battery: {
        soc: 0,
        level: 0,
        capacity: 0,
      },
      updateTimer: null,
    }
  },

  mounted() {
    // eslint-disable-next-line no-unused-vars
    this.$socket.emit("getLatestRecords", (response) => {
      this.records = response.data
      this.getDashboardUpdate()
    })
  },

  methods: {
    getDashboardUpdate() {
      if (!this.stopUpdating) {
        this.updateTimer = setInterval(() => {
          this.$socket.emit("getDashboardUpdate", (response) => {
            
            this.records.voltage.push(response.data.voltage)
            this.records.input_current.push(response.data.input_current)
            this.records.output_current.push(response.data.output_current)
            this.records.soc.push(response.data.soc)

            this.battery.soc = response.data.soc
            this.battery.level = response.data.charging_level
            this.battery.capacity = response.data.capacity

            if (this.records.voltage.length >= 3 * 60) {
              this.records.voltage = this.records.voltage.slice(1)
              this.records.input_current = this.records.input_current.slice(1)
              this.records.output_current = this.records.output_current.slice(1)
              this.records.soc = this.records.soc.slice(1)
            }
          })
        }, 1000)
      }
    }
  },

  computed: {
    device() {
      return this.$store.state.device
    }
  },

  beforeDestroy() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer)
    }
  }
}
</script>