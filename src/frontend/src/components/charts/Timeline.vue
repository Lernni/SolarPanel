<template>
  <apexchart ref="timeline" height="150px" :options="chartOptions" :series="seriesData"></apexchart>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

var de = require("apexcharts/dist/locales/de.json")

export default {
  name: 'TimelineChart',
  components: {
    apexchart: VueApexCharts
  },
  props: ["seriesData"],
  data() {
    return {
      chartOptions: {
        chart: {
          locales: [de],
          defaultLocale: "de",
          type: 'rangeBar',
          toolbar: {
            tools: {
              reset: false,
              download: false
            }
          },
          events: {
            // eslint-disable-next-line no-unused-vars
            zoomed: function(chartContext, axis) {
              this.$emit("updateDateTimeRange", axis.xaxis)
            }.bind(this),

            // eslint-disable-next-line no-unused-vars
            beforeResetZoom: function(chartContext, options) {
              this.$emit("updateDateTimeRange")
            }.bind(this),

            // eslint-disable-next-line no-unused-vars
            scrolled: function(chartContext, axis) {
              this.$emit("updateDateTimeRange", axis.xaxis)
            }.bind(this),

            // eslint-disable-next-line no-unused-vars
            // dataPointSelection: function(event, chartContext, config) {
            //   this.$refs.timeline.zoomX(
            //     chartContext.rangeBar.seriesRangeStart[config.dataPointIndex],
            //     chartContext.rangeBar.seriesRangeEnd[config.dataPointIndex]
            //   )
            // }.bind(this)
          }
        },
        plotOptions: {
          bar: {
            horizontal: true
          }
        },
        xaxis: {
          type: 'datetime',
          min: undefined,
          max: undefined,
        },
        yaxis: {
          show: false
        }
      }
    }
  },

  methods: {
    updateChart(chartData) {
      this.$refs.timeline.updateSeries([{
        data: chartData
      }])
    },

    zoomX(start, end) {
      this.$refs.timeline.zoomX(start, end)
    },
  }
}
</script>
