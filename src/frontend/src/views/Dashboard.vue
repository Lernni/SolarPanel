<template>
  <b-row>
    <b-col>
      <b-card-group deck>
        <ParameterCard parameter="Spannung" unit="V" :seriesData=records.voltage />
        <ParameterCard parameter="Eingangsstrom" unit="A" color="#E91E63" :seriesData=records.input_current />
        <ParameterCard parameter="Ausgangsstrom" unit="A" color="#E91E63" :seriesData=records.output_current />
        <ParameterCard parameter="Eingangsleistung" unit="W" color="#546E7A" :seriesData=records.power />
      </b-card-group>
    </b-col>
    <!-- <div class="col-lg-4 col-md-6">
      <ParameterCard parameter="Ladezustand" color="#00ebb9">
        <div class="row battery-info no-gutters">
          <div class="col-lg-3 col-md-4">
            <Battery class="battery" :soc=63 />
          </div>
          <div class="col-lg-9 col-md-8">
            <h5>Kapazität</h5>
            <h2>80 Ah / 350 Ah</h2>
            <br><br>
            <h5>Vergleich zum Vortag</h5>
            <h2>+5 Ah</h2>
            <h4>+20%</h4>
          </div>
        </div>
      </ParameterCard>
    </div> -->
  </b-row>

</template>

<script>
import ParameterCard from '../components/ParameterCard.vue'
// import Battery from '../components/Battery.vue'

export default {
  name: 'Dashboard',
  components: {
    ParameterCard,
    // Battery
  },

  data() {
    return {
      records: {},
      updateTimer: null,
    }
  },

  mounted() {
    // eslint-disable-next-line no-unused-vars
    this.$socket.emit("getLatestRecords", (response) => {
      this.records = response.records
      this.records.power = []
      for (let i = 0; i < this.records.voltage.length; i++) {
        this.records.power[i] = (Math.round(this.records.voltage[i] * this.records.input_current[i] * 100) / 100).toFixed(2)
      }

      this.getLatestRecord()
    })
  },

  methods: {
    getLatestRecord() {
      if (!this.stopUpdating) {
        this.updateTimer = setInterval(() => {
          this.$socket.emit("getLatestRecord", (response) => {
            
            this.records.voltage.push(response.record.voltage)
            this.records.input_current.push(response.record.input_current)
            this.records.output_current.push(response.record.output_current)
            var power = (Math.round(response.record.voltage * response.record.input_current * 100) / 100).toFixed(2)
            this.records.power.push(power)

            if (this.records.voltage.length >= 60) {
              this.records.voltage = this.records.voltage.slice(1)
              this.records.input_current = this.records.input_current.slice(1)
              this.records.output_current = this.records.output_current.slice(1)
              this.records.power = this.records.power.slice(1)
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