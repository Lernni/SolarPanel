<script setup>
import Highcharts from 'highcharts'
import { onMounted, watch } from 'vue'

import { useUnits } from '../../modules/useUnits.js'

const props = defineProps({
  dataset: {
    type: Object,
    required: true,
  },
  options: {
    type: Object,
    default: () => ({}),
  },
})

const units = useUnits()

/**
 * Synchronize zooming through the setExtremes event handler.
 */
const syncExtremes = (e) => {
  var thisChart = this.chart

  if (e.trigger !== 'syncExtremes') {
    // Prevent feedback loop
    Highcharts.each(Highcharts.charts, function (chart) {
      if (chart !== thisChart) {
        if (chart.xAxis[0].setExtremes) {
          // It is null while updating
          chart.xAxis[0].setExtremes(e.min, e.max, undefined, false, { trigger: 'syncExtremes' })
        }
      }
    })
  }
}

const optionsTemplate = {
  chart: {
    marginLeft: 60,
    spacingTop: 30,
    spacingBottom: 20,
    height: '250px',
  },
  title: {
    align: 'left',
    margin: 0,
    x: 50,
  },
  credits: {
    enabled: false,
  },
  legend: {
    enabled: false,
  },
  xAxis: {
    crosshair: true,
    events: {
      setExtremes: syncExtremes,
    },
    type: 'datetime',
  },
  yAxis: {
    title: {
      text: null,
    },
  },
  tooltip: {
    borderWidth: 0,
    backgroundColor: 'none',
    pointFormat: '{point.y}',
    headerFormat: '',
    shadow: false,
    style: {
      fontSize: '14px',
    },
  },
  series: [],
}

const getOptions = (config) => {
  const options = { ...optionsTemplate }

  options.title.text = config.title
  options.yAxis.labels = { format: `{value} ${config.unit}` }
  options.series = [
    {
      data: config.data,
      name: config.name,
      type: config.type,
      color: config.color,
      tooltip: {
        valueSuffix: ' ' + config.unit,
      },
    },
  ]

  return options
}

watch(
  () => props.dataset,
  () => {
    if (!props.dataset) return

    const dataset = props.dataset

    document.getElementById('container').innerHTML = ''

    // prepare chart data
    for (const parameter of Object.keys(dataset.values)) {
      var chartDiv = document.createElement('div')
      chartDiv.className = 'chart'
      document.getElementById('container').appendChild(chartDiv)

      const chartData = dataset.values[parameter].map((value, index) => [
        dataset.timestamps[index] * 1000,
        value,
      ])

      console.log(chartData)

      const config = {
        title: units[parameter].text,
        data: chartData,
        name: parameter,
        type: 'spline',
        color: units[parameter].color,
        unit: units[parameter].unit,
      }

      Highcharts.chart(chartDiv, getOptions(config))
    }
  }
)

onMounted(() => {
  /**
   * In order to synchronize tooltips and crosshairs, override the
   * built-in events with handlers defined on the parent element.
   */
  ;['mousemove', 'touchmove', 'touchstart'].forEach(function (eventType) {
    document.getElementById('container').addEventListener(eventType, function (e) {
      var chart, point, i, event

      for (i = 0; i < Highcharts.charts.length; i = i + 1) {
        chart = Highcharts.charts[i]
        // Find coordinates within the chart
        event = chart.pointer.normalize(e)
        // Get the hovered point
        point = chart.series[0].searchPoint(event, true)

        if (point) {
          point.highlight(e)
        }
      }
    })
  })

  /**
   * Override the reset function, we don't need to hide the tooltips and
   * crosshairs.
   */
  Highcharts.Pointer.prototype.reset = function () {
    return undefined
  }

  /**
   * Highlight a point by showing tooltip, setting hover state and draw crosshair
   */
  Highcharts.Point.prototype.highlight = function (event) {
    event = this.series.chart.pointer.normalize(event)
    this.onMouseOver() // Show the hover marker
    this.series.chart.tooltip.refresh(this) // Show the tooltip
    this.series.chart.xAxis[0].drawCrosshair(event, this) // Show the crosshair
  }
})
</script>

<template>
  <div id="container"></div>
</template>
