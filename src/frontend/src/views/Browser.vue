<script setup>
import { computed } from 'vue'

import { SunIcon, DownloadIcon, ChipIcon } from '@heroicons/vue/solid'

import { useUnits } from '../modules/useUnits.js'
import { useBrowserStore } from '../stores/browser.js'
import ErrorMessage from '../components/UI/ErrorMessage.vue'
import SynchronizedCharts from '../components/browser/SynchronizedCharts.vue'

const units = useUnits()
const browserStore = useBrowserStore()

const noUnitsSelected = computed(() => browserStore.selectedUnits.length === 0)

const incorrectTimeRange = computed(() => {
  const start = browserStore.range.start
  const end = browserStore.range.end
  return end.isBefore(start) || start.isSame(end)
})

const sameDayRange = computed(() => {
  const start = browserStore.range.start
  const end = browserStore.range.end
  return start.isSame(end, 'day')
})

const validHoursStart = computed(() => {
  const maxValue = sameDayRange.value ? browserStore.range.end.utc().hours() : 23
  return {
    min: 0,
    max: maxValue,
  }
})

const validHoursEnd = computed(() => {
  const minValue = sameDayRange.value ? browserStore.range.start.utc().hours() : 0
  return {
    min: minValue,
    max: 23,
  }
})

const fetchData = async () => {
  browserStore.fetchData()
}
</script>

<template>
  <div class="w-full sm:w-5/6">
    <div class="divide-y rounded-xl bg-gray-50 p-3 shadow">
      <div>
        <div
          class="flex flex-col items-center justify-center space-y-8 pb-2 lg:flex-row lg:items-start lg:space-y-0 lg:space-x-8"
        >
          <div>
            <div class="mb-1 text-lg">Zeitraum</div>
            <div class="flex flex-col items-center space-y-4 sm:flex-row sm:space-y-0 sm:space-x-4">
              <div>
                <v-date-picker v-model="browserStore.timeRange" timezone="UTC" is-range />
              </div>
              <div
                class="flex flex-col justify-center"
                :class="incorrectTimeRange ? 'invalid' : ''"
              >
                <label>Startzeit</label>
                <v-date-picker
                  v-model="browserStore.startTime"
                  :valid-hours="validHoursStart"
                  mode="time"
                  class="mb-3"
                  timezone="UTC"
                  is24hr
                />
                <label>Endzeit</label>
                <v-date-picker
                  v-model="browserStore.endTime"
                  :valid-hours="validHoursEnd"
                  mode="time"
                  timezone="UTC"
                  is24hr
                />
              </div>
            </div>
          </div>
          <div>
            <div class="mb-1 text-lg">Messgrößen</div>
            <div
              v-for="(value, key) in units"
              :key="key"
              class="flex"
              :class="noUnitsSelected ? 'invalid' : ''"
            >
              <input
                :id="key"
                v-model="browserStore.selectedUnits"
                :value="key"
                type="checkbox"
                class="mb-2 h-6 w-6 rounded border-gray-300 text-indigo-600"
              />
              <label :for="key" class="ml-2">{{ value.text }}</label>
            </div>
          </div>
        </div>
        <p class="text-sm text-slate-500">
          Alle Zeitangaben sind in mitteleuropäischer Winterzeit (UTC+1)
        </p>
        <ErrorMessage v-show="incorrectTimeRange"
          >Bitte gebe einen gültigen Zeitraum an!</ErrorMessage
        >
        <ErrorMessage v-show="noUnitsSelected">Wähle mindestens eine Messgröße aus!</ErrorMessage>
      </div>
      <div class="flex justify-center py-4">
        <button
          class="button-md"
          :disabled="incorrectTimeRange || noUnitsSelected"
          @click="fetchData"
        >
          <SunIcon class="inline h-6 w-6" />
          <span class="ml-1">Abfrage</span>
        </button>
        <button class="button-md ml-2" disabled>
          <DownloadIcon class="inline h-6 w-6" />
          <span class="ml-1">Download</span>
        </button>
        <button class="button-md ml-2" disabled>
          <ChipIcon class="inline h-6 w-6" />
          <span class="ml-1">Export (USB)</span>
        </button>
      </div>
      <div>
        <h2 class="my-4 text-center text-lg text-gray-700">
          <span v-if="browserStore.hasResults">
            Ergebnisse vom
            <span class="font-semibold">{{
              browserStore.datasetRange.start.format('DD.MM.YY HH:mm:ss')
            }}</span>
            bis
            <span class="font-semibold">
              {{ browserStore.datasetRange.end.format('DD.MM.YY HH:mm:ss') }}</span
            >
          </span>
          <span v-else>Keine Ergebnisse</span>
        </h2>
        <SynchronizedCharts :dataset="browserStore.dataset" />
      </div>
    </div>
  </div>

  <!---->
</template>
