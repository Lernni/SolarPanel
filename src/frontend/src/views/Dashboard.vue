<template>
  <div class="row">
    <div class="col-lg-8 col-md-6">
      <div class="card-deck">
        <ParameterCard parameter="Spannung" unit="V" :seriesData=records.voltage />
        <ParameterCard parameter="Eingangsstrom" unit="mA" color="#E91E63" :seriesData=records.input_current />
        <ParameterCard parameter="Ausgangsstrom" unit="A" color="#E91E63" :seriesData=records.output_current />
        <ParameterCard parameter="Leistung" unit="W" color="#546E7A" :seriesData=records.power />
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
  computed: {
    records () {
      return this.$store.state.records
    }
  }
}
</script>

<style lang="scss">
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