<template>
  <div class="row">
    {{ device }}
    <div class="col-lg-8 col-md-6">
      <div class="card-deck">
        <ParameterCard parameter="Spannung" unit="V" :seriesData=records.voltage />
        <ParameterCard parameter="Eingangsstrom" unit="mA" color="#E91E63" :seriesData=records.input_current />
        <ParameterCard parameter="Ausgangsstrom" unit="A" color="#E91E63" :seriesData=records.output_current />
        <ParameterCard parameter="Eingangsleistung" unit="W" color="#546E7A" :seriesData=records.power />
      </div>
    </div>
    <div class="col-lg-4 col-md-6">
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
    </div>
  </div>

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

  mounted() {
    // eslint-disable-next-line no-unused-vars
    this.$socket.emit("getLatestRecords", (response) => {
      // this.records = response.records
      // this.records.power = []
      // for (let i = 0; i < this.records.voltage.length; i++) {
      //   this.records.power[i] = this.records.voltage[i] * this.records.records.input_current[i]
      // }

      this.getLatestRecord()
    })
  },

  methods: {
    async getLatestRecord() {
      await new Promise(resolve => setTimeout(resolve, 1000));
      this.$socket.emit("getLatestRecord", (response) => {
        this.records.voltage = this.records.voltage.slice(1)
        this.records.voltage.push(response.record.voltage)

        this.records.input_current = this.records.input_current.slice(1)
        this.records.input_current.push(response.record.input_current)

        this.records.output_current = this.records.output_current.slice(1)
        this.records.output_current.push(response.record.output_current)

        this.records.power = this.records.power.slice(1)
        this.records.power.push(response.record.voltage * response.record.input_current)

        this.getLatestRecord()
      })
    }
  },

  computed: {
    device() {
      return this.$store.state.device
    }
  }
}
</script>

<style lang="scss" scoped>
.battery-info {
  margin-bottom: 25px;
  margin-top: 25px;

  h4, h2 {
    text-align: right;
  }

  h2, h4, h5 {
    display: block;
    float: none;
  }
}

.battery {
  margin-left: auto;
  margin-right: auto;
}
</style>