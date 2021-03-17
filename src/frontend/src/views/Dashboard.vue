<template>
  <div class="row">
    <div class="col-lg-8 col-md-6">
      <div class="card-deck">
        <ParameterCard parameter="Spannung" :value=voltage unit="V"/>
        <ParameterCard parameter="Eingangsstrom" :value=input_current unit="A" color="#E91E63"/>
        <ParameterCard parameter="Ausgangsstrom" :value=output_current unit="A" color="#E91E63"/>
        <ParameterCard parameter="Leistung" :value=power unit="W" color="#546E7A"/>
      </div>
    </div>
    <div class="col-lg-4 col-md-6">
      <ParameterCard parameter="Ladezustand" color="#00ebb9">
        <div class="row battery-info no-gutters">
          <div class="col-lg-3 col-md-4">
            <Battery class="battery" soc="63"/>
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
import axios from 'axios'

export default {
  name: 'Dashboard',
  components: {
    ParameterCard,
    Battery
  },
  data() {
    return {
      voltage: 0,
      input_current: 0,
      output_current: 0,
      power: 0
    };
  },
  async mounted() {
    await axios({ method: "GET", "url": "http://localhost/solarmodule"}).then(result => {
      this.voltage = result.data['voltage'];
      this.input_current = result.data['input_current'];
      this.output_current = result.data['output_current'];
      this.power = result.data['power'];
    }, error => {
      console.error(error);
    });
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