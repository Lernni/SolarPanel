<script setup>
import { onMounted, ref, watch } from 'vue'

const chartRef = ref(null)

const props = defineProps({
  seriesName: { type: String, default: 'Series' },
  seriesData: { type: Array, default: () => [] },
  unit: { type: String, default: '-' },
})

const chartOptions = {
  chart: {
    type: 'area',
    backgroundColor: null,
    animation: false,
  },
  title: {
    style: {
      display: 'none',
    },
  },
  credits: {
    enabled: false,
  },
  xAxis: {
    labels: {
      enabled: false,
    },
  },
  yAxis: {
    labels: {
      enabled: false,
    },
    title: {
      enabled: false,
    },
  },
  legend: {
    enabled: false,
  },
  tooltip: {
    hideDelay: 0,
    outside: true,
    shared: true,
    formatter: function () {
      return this.y + ' ' + props.unit
    },
  },
  series: [
    {
      name: props.seriesName,
      data: props.seriesData,
    },
  ],
}

onMounted(() => {
  console.log('mounted')
  watch(props.seriesData, () => {
    chartRef.value.chart.series[0].setData(props.seriesData, true, false)
  })
})
</script>

<template>
  <highcharts ref="chartRef" :options="chartOptions" style="height: 200px"></highcharts>
</template>
