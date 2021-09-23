<template>
  <b-card>
    <h5 class="card-title">{{parameter}}</h5>
    <slot></slot>
    <h2 class="text-right">{{seriesData[seriesData.length - 1]}} {{unit}}</h2>
    <Sparkline ref="sparkline" :height="($screen.width <= 450) ? 50 : 100" :series="series" :unit="unit"/>
  </b-card>
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
        color: this.color,
      }]
    }
  },
  watch: {
    seriesData: {
      // eslint-disable-next-line no-unused-vars
      handler: function(newVal, oldVal) {
        this.$refs.sparkline.updateChart(newVal)
      },
      deep: true
    }
  }
}
</script>

<style lang="scss" scoped>

  .sparkline {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    margin-left: auto;
    margin-right: auto;
  }

  .card {
    width: 100%;
    flex: none !important;
    margin: 5px;

    .card-body {
      padding-bottom: 50px;
    }
    
    h5, h2 {
      display: inline;
    }

    h2 {
      float: right;
    }
  }

  @media (min-width: 450px) {
    .card .card-body {
      padding-bottom: 100px;
    }
  }

  @media (min-width: 992px) {
    .card {
      max-width: 300px;
      
      h5, h2 {
        display: block;
      }

      h2 {
        float: none;
      }
    }
  }
</style>