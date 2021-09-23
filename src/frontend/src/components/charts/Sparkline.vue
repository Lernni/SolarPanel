<template>
  <apexchart ref="chart" :series="series" :height="height" class="sparkline" type="area" :options="chartOptions"/>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

export default {
  name: 'SparklineChart',
  components: {
    apexchart: VueApexCharts
  },
  props: ["height", "series", "unit"],
  data() {
    return {
      chartOptions: {
        chart: {
          type: 'area',
          sparkline: {
            enabled: true
          },
          animations: {
            enabled: false,
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        tooltip: {
          enabled: false
        }
      }
    }
  },
  methods: {
    updateChart(chartData) {
      this.$refs.chart.updateSeries([{
        data: chartData
      }])
    }
  }
}
</script>