<template>
  <b-card>
    <h5 class="card-title">{{parameter}}</h5>
    <slot></slot>
    <div class="param-value text-right">{{seriesData[seriesData.length - 1]}} {{unit}}</div>
    <Sparkline ref="sparkline" :height="height" :series="series" :unit="unit"/>
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
  computed: {
    height() {
      if (this.$screen.width == 800) {
        return 40
      } else if (this.$screen.width <= 450) {
        return 50
      } else {
        return 100
      }
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
    margin: 5px !important;

    .card-body {
      padding-bottom: 50px;
    }
    
    h5, .param-value {
      display: inline;
    }

    .param-value {
      float: right;
      font-size: 1.25rem;
      font-weight: 500;
    }
  }

  @media (min-width: 450px) {
    .card {
      
      .card-body {
        padding-bottom: 100px;
      }

      .param-value {
        font-weight: 400;
        font-size: 2rem;
      }
    }
  }

  @media (min-width: 800px) and (max-width: 800px) and
  (min-height: 480px) and (max-height: 480px) {
    .sparkline {
      position: absolute;
      width: 11rem;
      margin-right: 0;
      margin-left: auto;
      height: 20px;
      top: 0;
      bottom: 0;
    }

    .card {
      border: none;
      
      .card-body {
        padding: 0.5rem;
        padding-right: 12rem;
      }

      .param-value {
        float: right;
        font-size: 1.25rem;
        font-weight: 500;
      }
    }
  }

  @media (min-width: 992px) {
    .card {
      max-width: 300px;
      
      h5, .param-value {
        display: block;
      }

      .param-value {
        float: none;
      }
    }
  }
</style>