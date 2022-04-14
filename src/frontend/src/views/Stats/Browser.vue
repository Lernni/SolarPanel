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
                <b-col xl="10" class="mt-3">
                  <div>
                    <b-row>
                      <b-col cols="12" sm="6">
                        <label for="start-datepicker">Startdatum</label>
                        <b-form-datepicker
                          id="start-datepicker"
                          v-model="startDate"
                          class="mb-2"
                          locale="de-DE"
                          :start-weekday="1"
                          :max="maxStartDate"
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
                      <b-col cols="12" sm="6">
                        <label for="end-datepicker">Enddatum</label>
                        <b-form-datepicker
                          id="end-datepicker"
                          v-model="endDate"
                          class="mb-2"
                          locale="de-DE"
                          :start-weekday="1"
                          :min="minEndDate"
                          :max="new Date()"
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
                <b-col>
                  <b-form-group>
                    <b-form-checkbox-group
                      id="unit-group1"
                      v-model="units.selected"
                      :options="units.options"
                      stacked
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
import SyncedBrowserChart from '../../components/charts/SyncedBrowserChart.vue'
//import OverlapBrowserChart from '../../components/charts/OverlapBrowserChart.vue'
import { required } from 'vuelidate/lib/validators'
import moment from 'moment-timezone'

export default {
  name: "Browser",
  components: {
      PillTab, SyncedBrowserChart //OverlapBrowserChart
  },

  data() {
    return {
      loadingEntities: true,
      firstRequest: true,
      loadingRequest: false,
      updateAvailable: false,
      timeRangeSubtext: 'Auswahl treffen',
      timeRangeDone: true,

      dateTimeRange: {
        start: moment.utc().add(1, 'h').subtract(1, 'd').set({seconds: 0}),
        end: moment.utc().add(1, 'h').set({seconds: 0})
      },

      maxStartDate: moment.utc().add(1, 'h').subtract(1, 'd').toDate(),
      minEndDate: moment.utc().add(1, 'h').toDate(),

      units: {
        selected: [],
        options: [
          { text: "Spannung (V)", value: "voltage" },
          { text: "Eingangsstrom (A)", value: "input_current" },
          { text: "Ausgangsstrom (A)", value: "output_current" },
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
    units: {
      selected: {
        required
      }
    }
  },

  mounted() {
    this.dateTimeRangeUpdate()
  },

  computed: {
    startDate: {
      get() {
        return this.dateTimeRange.start.toDate()
      },
      set(date) {
        let pickedDate = moment.utc(date)
        this.dateTimeRange.start.set({
          year: pickedDate.year(),
          month: pickedDate.month(),
          date: pickedDate.date()
        })
        this.dateTimeRangeUpdate()
      }
    },

    endDate: {
      get() {
        return this.dateTimeRange.end.toDate()
      },
      set(date) {
        let pickedDate = moment.utc(date)
        this.dateTimeRange.end.set({
          year: pickedDate.year(),
          month: pickedDate.month(),
          date: pickedDate.date()
        })
        this.dateTimeRangeUpdate()
      }
    },

    startTime: {
      get() {
        return this.dateTimeRange.start.format("HH:mm")
      },
      set(time) {
        let pickedTime = moment(time, "HH:mm")
        this.dateTimeRange.start.set({
          hour: pickedTime.hour(),
          minute: pickedTime.minute(),
          seconds: 0,
        })
        this.dateTimeRangeUpdate()
      }
    },
    
    endTime: {
      get() {
        return this.dateTimeRange.end.format("HH:mm")
      },
      set(time) {
        let pickedTime = moment(time, "HH:mm")
        this.dateTimeRange.end.set({
          hour: pickedTime.hour(),
          minute: pickedTime.minute(),
          seconds: 0,
        })
        this.dateTimeRangeUpdate()
      }
    },

    unitsSubtext: function() {
      if (this.unitsDone) {
        return this.units.selected.length + " ausgewählt"
      } else {
        return "Auswahl treffen"
      }
    },

    unitsDone: function() {
      return this.$v.units.selected.required
    },

    device() {
      return this.$store.state.device
    }
  },

  watch: {
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
            case "soc":
              chartOptions = this.getChartOptions("Ladezustand", "Ah", "line", "#00EBB9")
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

    dateTimeRangeUpdate() {
      this.maxStartDate = this.dateTimeRange.end.toDate()
      this.minEndDate = this.dateTimeRange.start.toDate()
      this.timeRangeDone = this.dateTimeRange.start < this.dateTimeRange.end
      this.setTimeRangeSubtext()
    },

    setTimeRangeSubtext() {
      if (this.timeRangeDone) {
        this.timeRangeSubtext = [
          this.dateTimeRange.start.format("DD.MM.YYYY HH:mm"),
          this.dateTimeRange.end.format("DD.MM.YYYY HH:mm")
        ]
      } else {
        this.timeRangeSubtext = "Auswahl treffen"
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
          start_time: this.dateTimeRange.start.format("YYYY-MM-DD_HH-mm"),
          end_time: this.dateTimeRange.end.format("YYYY-MM-DD_HH-mm"),
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