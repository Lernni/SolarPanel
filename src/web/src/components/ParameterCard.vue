<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{{parameter}}</h5>
      <slot></slot>
      <h2 class="text-right">{{value}} {{unit}}</h2>
      <apexchart class="sparkline d-none d-lg-block" type="area" height="100" :options="chartOptions" :series="series"></apexchart>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'

export default {
  name: 'ParameterCard',
  components: {
    apexchart: VueApexCharts
  },
  props: {
    parameter: String,
    value: Number,
    unit: String,
    color: String
  },
  data: (instance) => ({
    series: [{
      name: instance.parameter,
      data: [31, 40, 28, 51, 42, 109, 100],
      color: instance.color,
    }],
    chartOptions: {
      chart: {
        type: 'area',
        sparkline: {
          enabled: true
        }
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        curve: 'smooth'
      },
      tooltip: {
        x: {
          format: 'dd/MM/yy HH:mm'
        },
      },
    },
  })
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