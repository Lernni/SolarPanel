<template>
  <div id="browser">
    <b-row class="justify-content-center">
      <b-col xl="10">
        <b-card no-body>
          <b-tabs pills card :vertical="$screen.lg" nav-wrapper-class="xl-2" class="flex-nowrap">
            <PillTab caption="Zeitraum" :done="timeRangeDone" :disabled="loadingRequest">
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
              <b-row class="justify-content-center">
                <b-col class="d-none d-sm-block" cols="12">
                  <b-skeleton-wrapper :loading="loadingEntities">
                    <template #loading>
                      <b-skeleton-img no-aspect height="150px"></b-skeleton-img>
                    </template>
                  </b-skeleton-wrapper>
                  <!-- Timeline must be outside of skeleton-wrapper, because Timeline will be undefined otherwise, as long as loadingEntities = true -->
                  <Timeline v-show="!loadingEntities" @updateDateTimeRange="updateDateTimeRange" ref="timeline" />
                </b-col>
                <b-col xl="10" class="mt-3">
                  <div>
                    <b-row>
                      <b-col cols="12" sm="6">
                        <label for="start-datepicker">Startdatum</label>
                        <b-form-datepicker
                          id="start-datepicker"
                          v-model="startDateModel"
                          class="mb-2"
                          locale="de-DE"
                          :start-weekday="1"
                          :max="dateTimeRange.end"
                          labelHelp=""
                          labelNoDateSelected="Kein Datum ausgewählt"
                          :state="timeRangeDone"
                        ></b-form-datepicker>
                      </b-col>
                      <b-col>
                        <label for="start-timepicker">Startzeit</label>
                        <b-form-input
                          id="input"
                          v-model="startTimeModel"
                          type="time"
                          class="mb-2"
                          :state="timeRangeDone"
                        ></b-form-input>
                      </b-col>
                    </b-row>
                    <b-row>
                      <b-col cols="12" sm="6">
                        <label for="end-datepicker">Enddatum</label>
                        <b-form-datepicker
                          id="end-datepicker"
                          v-model="endDateModel"
                          class="mb-2"
                          locale="de-DE"
                          :start-weekday="1"
                          :min="dateTimeRange.start"
                          :max="currentMEZTime.toDate()"
                          labelHelp=""
                          labelNoDateSelected="Kein Datum ausgewählt"
                          :state="timeRangeDone"
                        ></b-form-datepicker>
                      </b-col>
                      <b-col>
                        <label for="end-timepicker">Endzeit</label>
                        <b-form-input
                          id="end-timepicker"
                          v-model="endTimeModel"
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
                  </div>
                </b-col>
              </b-row>
            </PillTab> 

            <PillTab caption="Messgrößen" :done="unitsDone" :disabled="loadingRequest">
              <template #tab-content>
                {{ unitsSubtext }}
              </template>

              Ausgewählte Messgrößen können im Diagramm beliebig ein- und ausgeblendet werden.
              <br><br>
              <b-row>
                <b-col cols="6" xl="4">
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
                      disabled
                    ></b-form-checkbox-group>
                  </b-form-group>
                </b-col>
              </b-row>
            </PillTab>

            <b-tab :disabled="!timeRangeDone || !unitsDone" @click="handleRequestClick" title-item-class="align-self-center">
              <template #title>
                <b-row align-v="center">
                  <b-col cols="auto" class="pr-0 d-flex align-items-center">
                    <b-spinner small type="grow" v-show="loadingRequest"></b-spinner>
                    <b-button
                      v-show="updateAvailable && !loadingRequest"
                      size="sm"
                      variant="warning"
                      v-b-tooltip.hover.bottom="'Aktualisieren'"
                      @click="requestRecords"
                    >
                      <b-icon-arrow-repeat></b-icon-arrow-repeat>
                    </b-button>
                  </b-col>
                  <b-col>
                    <div class="text-center">
                      <h5>Auswertung</h5>
                    </div>
                  </b-col>
                </b-row>
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

                <b-overlay :show="loadingRequest" spinner-type="grow">
                  <template #overlay>
                    <b-icon
                      icon="brightness-high-fill"
                      scale="4"
                      animation="spin"
                      variant="warning"
                    ></b-icon>
                  </template>

                  <div v-show="!loadingRequest">
                    <SyncedBrowserChart
                      v-show="chartType.selected === 'many'"
                      ref="syncedBrowserChart"
                      @updateDateTimeRange="checkForUpdateRequest"
                      :chartsData="browserSeries"
                    />

                    <!-- <OverlapBrowserChart
                      v-show="chartType.selected == 'one'"
                      ref="overlapBrowserChart"
                      @updateDateTimeRange="checkForUpdateRequest"
                      :seriesData="browserSeries"
                    /> -->
                  </div>

                </b-overlay>
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
import moment from 'moment-timezone'

export default {
  name: "Browser",
  components: {
      PillTab, Timeline, SyncedBrowserChart //OverlapBrowserChart
  },

  data() {
    return {

      enableZoomEvents: true,
      loadingEntities: true,
      firstRequest: true,
      loadingRequest: false,
      updateAvailable: false,

      currentMEZTime: moment.utc().add(1, 'h'),
      mStartTime: moment.utc(),
      mEndTime: moment.utc(),

      dateTimeRange: {
        start: Date.now(),
        end: Date.now()
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

      browserSeries: [],
    }
  },

  validations: {
    dateTimeRange: {
      minValue: value => {
        if (value === undefined) return false
        return value.end > value.start
      }
    },

    units: {
      selected: {
        required
      }
    }
  },

  mounted() {
    this.mStartTime = this.currentMEZTime.clone().subtract(1, 'days')
    this.mEndTime = this.currentMEZTime.clone()

    this.dateTimeRange.start = this.mStartTime.toDate()
    this.dateTimeRange.end = this.mEndTime.toDate()

    if (this.device == "External") {
      const interval = setInterval(() => {
        if (this.$refs.timeline) {
          this.$refs.timeline.zoomX(this.dateTimeRange.start, this.dateTimeRange.end)
          clearInterval(interval)
        }
      }, 50)

      this.$socket.emit("getDBSections", {
        start_time: this.mStartTime.valueOf(),
        end_time: this.mEndTime.valueOf()
      }, (response) => {
        this.loadingEntities = false
        this.entities = []
  
        for (let i = 0; i < response.data.length; i++) {
          this.entities.push({
            x: "records",
            y: [response.data[i][0] * 1000, response.data[i][1] * 1000],
          })
        }
  
        this.$refs.timeline.updateChart(this.entities)

        this.mStartTime = moment.utc(this.entities[0].y[0])
        this.mEndTime = moment.utc(this.entities[this.entities.length - 1].y[1])

        this.dateTimeRange.start = this.mStartTime.valueOf()
        this.dateTimeRange.end = this.mEndTime.valueOf()
      })
    }
  },

  computed: {
    startDateModel: {
      get() {
        return this.mStartTime.toDate()
      },
      set(date) {
        let pickedDate = moment.utc(date)
        this.mStartTime = this.mStartTime
          .year(pickedDate.year())
          .month(pickedDate.month())
          .date(pickedDate.date())

        this.dateTimeRange.start = this.mStartTime.valueOf()
      }
    },

    endDateModel: {
      get() {
        return this.mEndTime.toDate()
      },
      set(date) {
        let pickedDate = moment.utc(date)
        this.mEndTime = this.mEndTime
          .year(pickedDate.year())
          .month(pickedDate.month())
          .date(pickedDate.date())

        this.dateTimeRange.end = this.mEndTime.valueOf()
      }
    },

    startTimeModel: {
      get() {
        return this.mStartTime.format("HH:mm")
      },
      set(time) {
        let pickedTime = moment(time, "HH:mm")
        this.mStartTime = this.mStartTime
          .hours(pickedTime.hours())
          .minutes(pickedTime.minutes())

        this.dateTimeRange.start = this.mStartTime.valueOf()
      }
    },
    
    endTimeModel: {
      get() {
        return this.mEndTime.format("HH:mm")
      },
      set(time) {
        let pickedTime = moment(time, "HH:mm")
        this.mEndTime = this.mEndTime
          .hours(pickedTime.hours())
          .minutes(pickedTime.minutes())

        this.dateTimeRange.end = this.mEndTime.valueOf()
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
        return [
          this.mStartTime.format("DD.MM.YYYY HH:mm"),
          this.mEndTime.format("DD.MM.YYYY HH:mm")
        ]
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

    device() {
      return this.$store.state.device
    }
  },

  watch: {
    dateTimeRange: {
      // eslint-disable-next-line no-unused-vars
      handler: function(newVal, oldVal) {
        this.enableZoomEvents = false
        this.$refs.timeline.zoomX(newVal.start, newVal.end)
        this.enableZoomEvents = true

        this.checkForUpdateRequest()
      },
      deep: true
    },

    "units.selected"() {
      this.checkForUpdateRequest()
    }
  },

  methods: {
    setDBRecords(data) {
      if (this.loadingRequest) {
        this.browserSeries = []


        let chartOptions = {}

        for (let i = 0; i < this.units.selected.length; i++) {
          switch (this.units.selected[i]) {
            case "voltage":
              chartOptions = this.getChartOptions("Spannung", "V", "line", "#2E93FA")
              break
            case "input_current":
              chartOptions = this.getChartOptions("Eingangsstrom", "A", "line", "#E91E63")
              break
            case "output_current":
              chartOptions = this.getChartOptions("Ausgangsstrom", "A", "line", "#E91E63")
              break
          }

          chartOptions.name = this.units.selected[i]
          let seriesData = []

          for (let section of data) {
            for (let record of section) {
              seriesData.push({
                x: record[0] * 1000,
                y: record[i + 1]
              })
            }

            seriesData.push({
              x: section[section.length - 1][0] * 1000 + 1,
              y: null
            })
          }

          chartOptions.series = [{ data: seriesData }]

          this.browserSeries.push(chartOptions)
        }

        this.$refs.syncedBrowserChart.updateChart(this.browserSeries)
        this.loadingRequest = false
      }
    },

    getChartOptions(title, unit, lineType, color) {
      return {
        title: title,
        unit: unit,
        options: {
          chart: {
            type: lineType,
          },
          colors: [color],
        }
      }
    },

    updateDateTimeRange(range) {
      if (this.enableZoomEvents) {
        this.mStartTime = moment.utc(range.min)
        this.mEndTime = moment.utc(range.max)

        this.dateTimeRange.start = this.mStartTime.valueOf()
        this.dateTimeRange.end = this.mEndTime.valueOf()
      }
    },

    checkForUpdateRequest() {
      this.updateAvailable = (this.timeRangeDone && this.unitsDone && !this.firstRequest)
    },

    handleRequestClick() {
      if (this.firstRequest) {
        this.firstRequest = false
        this.requestRecords()
      }
    },

    requestRecords() {
      this.updateAvailable = false
      this.loadingRequest = true
      this.browserSeries = []

      this.$socket.emit("browserRequest",
        {
          start_time: this.mStartTime.subtract(1, "hours").valueOf(),
          end_time: this.mEndTime.subtract(1, "hours").valueOf(),
          units: this.units.selected
        }, (response) => {
        this.setDBRecords(response.data)
      })
    }
  }
}
</script>

<style lang="scss">
  #browser {
    h5 {
      margin-bottom: 0 !important;
    }
    .col-2-5 {
      flex: 0 0 20%;
      max-width: 20%;
    }

    .nav {
      justify-content: center;
    }
  }

  @media (min-width: 992px) {
    #browser {
      .nav {
        justify-content: flex-start;
      }
    }
  }

  @media (max-width: 1520px) {
    #browser {
      .time-options {
        flex: 0 0 100%;
        max-width: 100%;
        width: 100%;
      }
    }
  }
</style>