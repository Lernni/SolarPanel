<template>
  <apexchart class="sparkline" type="area" :height="height" :options="chartOptions" :series="series"/>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts'

export default {
  name: 'Sparkline Chart',
  components: {
    apexchart: VueApexCharts
  },
  props: {
    height: Number,
    series: Array
  },
  data: (instance) => (
    instance.series, {
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
      }
    }
  })
}
</script>

<style>

</style>