<template>
  <div>
    <b-row class="justify-content-center">
      <b-col cols="11">
        <h3>Zeitraum</h3>
        <b-row>
          <b-col cols="7">
            <apexchart ref="timeline" type="rangeBar" height="150px" :options="chartOptions" :series="series"></apexchart>
          </b-col>
          <b-col>
            <b-row>
              <b-col>
                <label for="start-datepicker">Startdatum</label>
                <b-form-datepicker
                  id="start-datepicker"
                  v-model="startDate"
                  class="mb-2"
                  locale="de-DE"
                  :start-weekday="1"
                  :max="endDate"
                  labelHelp=""
                  labelNoDateSelected="Kein Datum ausgewählt"
                ></b-form-datepicker>
              </b-col>
              <b-col>
                <label for="start-timepicker">Startzeit</label>
                <b-form-input id="input" v-model="startTime" type="time" class="mb-2"></b-form-input>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <label for="end-datepicker">Enddatum</label>
                <b-form-datepicker
                  id="end-datepicker"
                  v-model="endDate"
                  class="mb-2"
                  locale="de-DE"
                  :start-weekday="1"
                  :min="startDate"
                  :max="maxDate"
                  labelHelp=""
                  labelNoDateSelected="Kein Datum ausgewählt"
                ></b-form-datepicker>
              </b-col>
              <b-col>
                <label for="end-timepicker">Endzeit</label>
                <b-form-input id="end-timepicker" v-model="endTime" type="time" class="mb-2"></b-form-input>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        <h3>Messgrößen</h3>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'

var de = require("apexcharts/dist/locales/de.json")

const Formatter = {
  toTime: function(dateTime) {
    return ("0" + new Date(dateTime).getHours()).slice(-2) + ":" + ("0" + new Date(dateTime).getMinutes()).slice(-2)
  }
}

export default {
  name: "Browser",
  components: {
      apexchart: VueApexCharts,
  },
  data() {
    return {

      maxDate: new Date(),
      enableZoomEvents: true,

      dateTimeRange: {
        min: Date.now(),
        max: Date.now(),
      },

      // timeline

      series: [
        {
          data: [
            {
              x: "records",
              y: [
                new Date('2019-03-02').getTime(),
                new Date('2019-03-04').getTime(),
              ]
            },
            {
              x: "records",
              y: [
                new Date('2019-03-08').getTime(),
                new Date('2019-03-09').getTime(),
              ]
            },
            {
              x: "records",
              y: [
                new Date('2019-04-02').getTime(),
                new Date('2019-05-04').getTime(),
              ]
            },
            {
              x: "records",
              y: [
                new Date('2019-08-12').getTime(),
                new Date('2019-08-20').getTime(),
              ]
            },
          ]
        }
      ],
      chartOptions: {
        chart: {
          locales: [de],
          defaultLocale: "de",
          height: "300px",
          type: 'rangeBar',
          toolbar: {
            tools: {
              download: false
            }
          },
          events: {
            // eslint-disable-next-line no-unused-vars
            zoomed: function(chartContext, axis) {
              this.updateDateTimeRange(axis.xaxis)
            }.bind(this),

            // eslint-disable-next-line no-unused-vars
           /* beforeResetZoom: function(chartContext, options) {
              console.log(options)
              this.updateDateTimeRange(options.config.xaxis)
            }.bind(this),*/

            // eslint-disable-next-line no-unused-vars
            scrolled: function(chartContext, axis) {
              this.updateDateTimeRange(axis.xaxis)
            }.bind(this),

            // eslint-disable-next-line no-unused-vars
            dataPointSelection: function(event, chartContext, config) {
              var dataPointRange = this.series[0].data[config.dataPointIndex].y
              this.$refs.timeline.zoomX(dataPointRange[0], dataPointRange[1])
            }.bind(this)
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
      },
    }
  },

  mounted() {
    this.$refs.timeline.zoomX(this.dateTimeRange.min, this.dateTimeRange.max)
  },
  computed: {
    startDate: {
      get: function() {
        return new Date(this.dateTimeRange.min)
      },
      set: function(date) {
        date = new Date(date)
        var startDateTime = new Date(this.dateTimeRange.min)

        console.log(date)
        console.log(date.getYear())
        startDateTime.setFullYear(date.getFullYear())
        startDateTime.setMonth(date.getMonth())
        startDateTime.setDate(date.getDate())

        this.dateTimeRange.min = startDateTime.getTime()
      }
    },

    startTime: {
      get: function() {
        return Formatter.toTime(this.dateTimeRange.min)
      },
      set: function(time) {
        var splittedTime = time.split(':')
        var startDateTime = new Date(this.dateTimeRange.min)

        startDateTime.setHours(splittedTime[0])
        startDateTime.setMinutes(splittedTime[1])

        this.dateTimeRange.min = startDateTime.getTime()
      }
    },

    endDate: {
      get: function() {
        return new Date(this.dateTimeRange.max)
      },
      set: function(date) {
        date = new Date(date)
        var endDateTime = new Date(this.dateTimeRange.max)

        endDateTime.setFullYear(date.getFullYear())
        endDateTime.setMonth(date.getMonth())
        endDateTime.setDate(date.getDate())

        this.dateTimeRange.max = endDateTime.getTime()
      }
    },

    endTime: {
      get: function() {
        return Formatter.toTime(this.dateTimeRange.max)
      },
      set: function(time) {
        var splittedTime = time.split(':')
        var endDateTime = new Date(this.dateTimeRange.max)

        endDateTime.setHours(splittedTime[0])
        endDateTime.setMinutes(splittedTime[1])

        this.dateTimeRange.max = endDateTime.getTime()
      }
    }
  },
  watch: {
    dateTimeRange: {
      // eslint-disable-next-line no-unused-vars
      handler: function(newVal, oldVal) {
        this.enableZoomEvents = false
        this.$refs.timeline.zoomX(newVal.min, newVal.max)
        this.enableZoomEvents = true
      },
      deep: true
    }
  },
  methods: {
    updateDateTimeRange(range) {
      if (this.enableZoomEvents) {
        this.dateTimeRange = range
      }
    }
  }
}
</script>

<style>

</style>