<template>
  <div>
    <b-row class="justify-content-center">
      <b-col cols="11">
        <b-card no-body>
          <b-tabs pills card vertical nav-wrapper-class="col-2" class="flex-nowrap">
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
                  <b-skeleton-wrapper :loading="loadingEntities">
                    <template #loading>
                      <b-skeleton-img no-aspect height="150px"></b-skeleton-img>
                    </template>
                  </b-skeleton-wrapper>
                  <!-- Timeline must be outside of skeleton-wrapper, because Timeline will be undefined otherwise, as long as loadingEntities = true -->
                  <Timeline v-show="!loadingEntities" @updateDateTimeRange="updateDateTimeRange" ref="timeline" :seriesData="entities" />
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
                  <h5>Auswertung</h5>
                </div>
              </template>
              <b-card-text>
                <b-form-group class="text-right">
                  Diagrammart:
                  <b-form-radio-group
                    id="chart-type-radio"
                    v-model="chartType.selected"
                    :options="chartType.options"
                    button-variant="outline-primary"
                    buttons
                  ></b-form-radio-group>
                </b-form-group>

                <SyncedBrowserChart
                  v-show="chartType.selected === 'many'"
                  ref="syncedBrowserChart"
                  @updateDateTimeRange="activateReload"
                  :chartsData="browserSeries"
                />

                <!--<OverlapBrowserChart
                  v-show="chartType.selected == 'one'"
                  ref="overlapBrowserChart"
                  @updateDateTimeRange="activateReload"
                  :seriesData="browserSeries"
                />-->

              </b-card-text>
            </b-tab>
          </b-tabs>
        </b-card>    
      </b-col>
    </b-row>
  </div>
</template>

<script>
import PillTab from '../../components/PillTab.vue'
import Timeline from '../../components/charts/Timeline.vue'
import SyncedBrowserChart from '../../components/charts/SyncedBrowserChart.vue'
//import OverlapBrowserChart from '../../components/charts/OverlapBrowserChart.vue'
import { required } from 'vuelidate/lib/validators'

const Formatter = {
  toTime: function(dateTime) {
    return ("0" + new Date(dateTime).getHours()).slice(-2) + ":" + ("0" + new Date(dateTime).getMinutes()).slice(-2)
  }
}

export default {
  name: "Browser",
  components: {
      PillTab, Timeline, SyncedBrowserChart, //OverlapBrowserChart
  },
  data() {
    return {

      maxDate: new Date(),
      enableZoomEvents: true,
      loadingEntities: true,


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

      chartType: {
        selected: "many",
        options: [
          { text: "Getrennt", value: "many" },
          { text: "Überlappend", value: "one" },
        ]
      },

      browserSeries: [
        {
          name: "voltage",
          title: "Spannung",
          unit: "V",
          options: {
            chart: {
              type: "line",
            },
            colors: ['#546E7A'],
          },
          series: [{
            data: [30, 40, 1, 50, 49, 4, 70, 81]
          }]
        },
        {
          name: "input-current",
          title: "Eingangsstrom",
          unit: "mA",
          options: {
            chart: {
              type: "line",
            },
            colors: ['#546E7A'],
          },
          series: [{
            data: [30, 40, 45, 50, 49, 60, 70, 81]
          }]
        },
        {
          name: "soc",
          title: "Ladezustand",
          unit: "Ah",
          options: {
            chart: {
              type: "area",
            },
            colors: ['#046E7A'],
          },
          series: [{
            data: [30, 40, 1, 50, 49, 60, 70, 81]
          }]
        },
      ],
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
    const interval = setInterval(() => {
      if (this.$refs.timeline) {
        this.$refs.timeline.zoomX(this.dateTimeRange.min, this.dateTimeRange.max)
        clearInterval(interval)
      }
    }, 50)
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

    entities() {
      return this.$store.state.entities
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
    },

    entities: {
      // eslint-disable-next-line no-unused-vars
      handler: function(newVal, oldVal) {
        const interval = setInterval(() => {
          if (this.$refs.timeline) {
            this.loadingEntities = false
            this.$refs.timeline.updateChart(newVal)
            this.dateTimeRange = {
              min: this.entities[0].y[0],
              max: this.entities[this.entities.length - 1].y[1]
            }
            clearInterval(interval)
          }
        }, 50)
      },
      deep: true
    },
  },

  methods: {
    updateDateTimeRange(range) {
      if (this.enableZoomEvents) {
        this.dateTimeRange = range
      }
    },

    activateReload() {

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