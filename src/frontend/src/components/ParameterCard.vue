<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{{parameter}}</h5>
      <slot></slot>
      <h2 class="text-right">{{unit}}</h2>
      <Sparkline ref="sparkline" :height=100 :series="series"/>
    </div>
  </div>
</template> 

<script>
import Sparkline from './charts/Sparkline.vue'

export default {
  name: 'ParameterCard',
  components: {
    Sparkline
  },
  props: ["parameter", "unit", "color", "seriesData"],
  data() {
    return {
      series: [{
        name: this.parameter,
        data: this.seriesData,
        color: this.color,
      }]
    }
  },
  watch: {
    seriesData: {
      handler: function(newVal, oldVal) {
        console.log("update" + oldVal + newVal)
        this.$refs.sparkline.updateChart(newVal)
      },
      deep: true
    }
  }
}
</script>

<style lang="scss">

  .sparkline {
    margin: 0 -20px -20px -20px;
  }

  .card {
    width: 100%;
    flex: none !important;
    margin: 5px;
    
    h5, h2 {
      display: inline;
    }

    h2 {
      float: right;
    }
  }

  @media (min-width: 992px) {
    .card {
      flex: 1 0 0% !important;
      margin: 0;

      h5, h2 {
        display: block;
      }

      h2 {
        float: none;
      }
    }
  }
</style>