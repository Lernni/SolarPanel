<template>
  <div>
    <b-row class="justify-content-center">
      <b-col cols="11">
        <h3>Zeitraum</h3>
        <b-row>
          <b-col cols="7">
            <apexchart type="rangeBar" height="150px" :options="chartOptions" :series="series"></apexchart>
          </b-col>
          <b-col>
            <b-row>
              <b-col>
                <label for="start-datepicker">Startdatum</label>
                <b-form-datepicker
                  id="start-datepicker"
                  v-model="form.startDate"
                  class="mb-2"
                  locale="de-DE"
                  :start-weekday="1"
                  :max="form.endDate"
                  labelHelp=""
                  labelNoDateSelected="Kein Datum ausgewählt"
                ></b-form-datepicker>
              </b-col>
              <b-col>
                <label for="start-timepicker">Startzeit</label>
                <b-form-input id="input" v-model="form.startTime" type="time" class="mb-2"></b-form-input>
              </b-col>
            </b-row>
            <b-row>
              <b-col>
                <label for="end-datepicker">Enddatum</label>
                <b-form-datepicker
                  id="end-datepicker"
                  v-model="form.endDate"
                  class="mb-2"
                  locale="de-DE"
                  :start-weekday="1"
                  :min="form.startDate"
                  :max="maxDate"
                  labelHelp=""
                  labelNoDateSelected="Kein Datum ausgewählt"
                ></b-form-datepicker>
              </b-col>
              <b-col>
                <label for="end-timepicker">Endzeit</label>
                <b-form-input id="end-timepicker" v-model="form.endTime" type="time" class="mb-2"></b-form-input>
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

const currentDate = new Date()
const currentTime = currentDate.getHours() + ":" +  currentDate.getMinutes()

export default {
  name: "Browser",
  components: {
      apexchart: VueApexCharts,
  },
  data() {
    return {

      maxDate: currentDate,

      form: {
        startDate: currentDate,
        endDate: currentDate,
        startTime: currentTime,
        endTime: currentTime
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
          height: "300px",
          type: 'rangeBar',
          toolbar: {
            tools: {
              download: false
            }
          },
          events: {
            // eslint-disable-next-line no-unused-vars
            beforeZoom: function(chartContext, axis) {
              console.log(axis.xaxis.min)
              this.form.startDate = new Date(axis.xaxis.min)
              this.form.endDate = new Date(axis.xaxis.max)
              this.form.startTime = this.form.startDate.getHours() + ":" + this.form.startDate.getMinutes()
              this.form.endTime = this.form.endDate.getHours() + ":" + this.form.endDate.getMinutes()
            }.bind(this)
          }
        },
        plotOptions: {
          bar: {
            horizontal: true
          }
        },
        xaxis: {
          type: 'datetime'
        },
        yaxis: {
          show: false
        }
      },
    }
  }
}
</script>

<style>

</style>