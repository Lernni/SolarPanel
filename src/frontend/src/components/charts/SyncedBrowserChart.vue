<template>
  <div>
    <div id="synced-charts" class="wrapper" v-for="chart in charts" :key="chart.name">
      <div :id="'chart-' + chart.name">
        <apexchart :ref="'chart-' + chart.name" height="150" :options="chart.options" :series="chart.series" />
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

var de = require("apexcharts/dist/locales/de.json")
var _ = require('lodash');

const varChartOptions = {
  toolbar: {
    tools: {
      zoomin: false,
      zoomout: false,
      pan: false,
      reset: false,
    }
  },
}

const fixChartOptions = {
  options: {
    chart: {
      group: "synced-charts",
      locales: [de],
      defaultLocale: "de",
    },
    xaxis: {
      //type: 'datetime',
      labels: {
        show: false
      },
      tooltip: {
        enabled: false
      }
    },
    yaxis: {
      labels: {
        minWidth: 40
      }
    },
    tooltip: {
      x: {
        show: false
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

export default {
  name: 'SyncedBrowserChart',
  components: {
    apexchart: VueApexCharts
  },
  props: ["chartsData"],

  data() {
    return {
      charts: this.chartsData
    }
  },

  created() {
    // init all requested synced charts
    for (var i = 0; i < this.charts.length; i++) {

      // set dyncamic chart options
      let title = this.charts[i].title;
      let unit = this.charts[i].unit;
      
      this.charts[i].options.yaxis = {
        title: {
          text: title + " (" + unit + ")"
        },
        labels: {
          formatter: function(val) {
            return val + " " + unit
          }
        }
      }

      this.charts[i].options.chart.id = "chart-" + i
      this.charts[i].series[0].name = title;

      this.charts[i].options.chart.events = {
        zoomed: function() {
          this.$emit("updateDateTimeRange")
        }.bind(this)
      }


      // merge fix chart options with specific chart options
      _.merge(this.charts[i].options, fixChartOptions.options)

      // only the first chart has the whole toolbar
      if (i != 0) this.charts[i].options.chart.toolbar = varChartOptions.toolbar
      // only the last chart has an x-axis
      if (i == this.charts.length - 1) {
        this.charts[i].options.xaxis.labels.show = true
        this.charts[i].options.xaxis.tooltip.enabled = true
      }
    }
  },

  methods: {
    selectionUpdate() {
      console.log("hey")
    }
  }
}
</script>
