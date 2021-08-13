<template>
  <apexchart ref="chart" :series="series" class="sparkline" type="area" :height="height" :options="chartOptions"/>
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
              enabled: true,
              easing: 'easeinout',
              speed: 1000,
              animateGradually: {
                  enabled: true,
                  delay: 150
              },
              dynamicAnimation: {
                  enabled: true,
                  speed: 1000
              }
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        tooltip: {
          style: {
            fontSize: "14px"
          },
          x: {
            formatter: function(value) {
              var secondsPassed = 60 - value + 1
              if (secondsPassed == 1) {
                return "vor einer Sekunde"
              } else if (secondsPassed == 60) {
                return "vor einer Minute"
              } else {
                return "vor " + secondsPassed + " Sekunden"
              }
            }
          },
          y: {
            formatter: function(value) {
              return value + " " + this.unit
            }.bind(this)
          }
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

<style>

</style>