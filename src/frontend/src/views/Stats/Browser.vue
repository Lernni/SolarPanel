<template>
  <div>
    <b-row class="justify-content-center">
      <b-col cols="11">
        <b-card no-body>
          <b-tabs pills card vertical nav-wrapper-class="col-2">
            <PillTab caption="Zeitraum" :done="timeRangeDone">
              <template #tab-content>
                <div v-show="timeRangeDone">
                  {{ timeRangeSubtext[0] }}
                  <br>
                  {{ timeRangeSubtext[1] }}
                </div>
                <div v-show="!timeRangeDone">
                  {{ timeRangeSubtext }}
                </div>
              </template>

              Alle Zeitangaben sind in mitteleuropäischer Winterzeit.
              <br><br>
              <b-row>
                <b-col cols="6">
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
                        :state="timeRangeDone"
                      ></b-form-datepicker>
                    </b-col>
                    <b-col>
                      <label for="start-timepicker">Startzeit</label>
                      <b-form-input
                        id="input"
                        v-model="startTime"
                        type="time"
                        class="mb-2"
                        :state="timeRangeDone"
                      ></b-form-input>
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
                        :state="timeRangeDone"
                      ></b-form-datepicker>
                    </b-col>
                    <b-col>
                      <label for="end-timepicker">Endzeit</label>
                      <b-form-input
                        id="end-timepicker"
                        v-model="endTime"
                        type="time"
                        class="mb-2"
                        :state="timeRangeDone"
                      ></b-form-input>
                    </b-col>
                  </b-row>
                  <b-row>
                    <b-col>
                      <b-form-invalid-feedback :state="timeRangeDone">
                        Enddatum muss größer als Startdatum sein!
                      </b-form-invalid-feedback>
                    </b-col>
                  </b-row>
                </b-col>
              </b-row>
            </PillTab>

            <PillTab caption="Messgrößen" :done="unitsDone">
              <template #tab-content>
                {{ unitsSubtext }}
              </template>

              Ausgewählte Messgrößen können im Diagramm beliebig ein- und ausgeblendet werden.
              <br><br>
              <b-row>
                <b-col cols="2">
                  <b-form-group>
                    <b-form-checkbox-group
                      id="unit-group1"
                      v-model="units.selected"
                      :options="units.options.slice(0, 3)"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-col>
                <b-col>
                  <b-form-group>
                    <b-form-checkbox-group
                      id="unit-group2"
                      v-model="units.selected"
                      :options="units.options.slice(3, 6)"
                      stacked
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-col>
              </b-row>
            </PillTab>

            <b-tab :disabled="!timeRangeDone || !unitsDone">
              <template #title>
                <div class="text-center">
                  <h5>Auswerten</h5>
                </div>
              </template>
              <b-card-text>Tab contents 2</b-card-text>
            </b-tab>
          </b-tabs>
        </b-card>    
      </b-col>
    </b-row>
  </div>
</template>

<script>
import VueApexCharts from 'vue-apexcharts'
import PillTab from '../../components/PillTab.vue'
import { required } from 'vuelidate/lib/validators'

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
      PillTab,
  },
  data() {
    return {

      maxDate: new Date(),
      enableZoomEvents: true,


      dateTimeRange: {
        min: Date.now(),
        max: Date.now(),
      },

      units: {
        selected: [],
        options: [
          { text: "Spannung (V)", value: "voltage" },
          { text: "Eingangsstrom (A)", value: "input_current" },
          { text: "Ausgangsstrom (A)", value: "output_current" },
          { text: "Eingangsleistung (W)", value: "input_power" },
          { text: "Ausgangsleistung (W)", value: "output_power" },
          { text: "Ladezustand (Ah)" , value: "soc" }
        ]
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

  validations: {
    dateTimeRange: {
      minValue: value => {
        if (value === undefined) return false
        return value.max > value.min
      }
    },
    units: {
      selected: {
        required
      }
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
    },

    unitsSubtext: function() {
      if (this.unitsDone) {
        return this.units.selected.length + " ausgewählt"
      } else {
        return "Auswahl treffen"
      }
    },

    timeRangeSubtext: function() {
      if (this.timeRangeDone) {
        return [new Date(this.dateTimeRange.min).toLocaleString(), new Date(this.dateTimeRange.max).toLocaleString()]
      } else {
        return "Auswahl treffen"
      }
    },

    timeRangeDone: function() {
      return this.$v.dateTimeRange.minValue
    },

    unitsDone: function() {
      return this.$v.units.selected.required
    },
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
  h5 {
    margin-bottom: 0 !important;
  },
  .col-2-5 {
    flex: 0 0 20%;
    max-width: 20%;
  }
</style>