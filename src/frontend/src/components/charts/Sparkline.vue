<template>
  <apexchart ref="schart" :series="series" class="sparkline" type="area" :height="height" :options="chartOptions"/>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: 'SparklineChart',
  components: {
    apexchart: VueApexCharts
  },
  props: ["height", "series"],
  data() {
    return {
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
    }
  },
  methods: {
    updateChart(chartData) {
      console.log("update chart")
      this.$refs.schart.updateSeries([{
        data: chartData
      }])
    }
  }
}
</script>

<style>

</style>