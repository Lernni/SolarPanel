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
import io from 'socket.io-client';

export default {
  name: 'Dashboard',
  components: {
    ParameterCard,
    Battery
  },
  data() {
    return {
      socket: io(),

      records: {
        voltage: [],
        input_current: [],
        output_current: [],
        power: []
      }
    }
  },
  // methods: {
  //   sendMessage() {
  //     this.socket.emit('testEvent', {
  //       message: '12345'
  //     });
  //     console.log("emitted test event")
  //   }
  // },


  created() {
    this.socket.on('latestRecords', (data) => {
      this.records.voltage = data.voltage;
      this.records.input_current = data.input_current;
      this.records.output_current = data.output_current;
    });

    this.socket.on("newRecord", (data) => {
      this.records.voltage = this.records.voltage.slice(1).push(data.voltage)
      this.records.input_current = this.records.input_current.slice(1).push(data.input_current)
      this.records.output_current = this.records.output_current.slice(1).push(data.output_current)
    })
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