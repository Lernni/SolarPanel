<script setup>
import HighscoreBar from './HighscoreBar.vue'
import SparklineChart from './SparklineChart.vue'
import { ref, watch } from 'vue'
import { useElementHover } from '@vueuse/core'
import { useDashboardStore } from '@/stores/dashboard'

const dashboardStore = useDashboardStore()

const props = defineProps({
  open: { type: Boolean, default: false },
  id: { type: String, default: 'id' },
  title: { type: String, default: 'Title' },
  unit: { type: String, default: '-' },

  minValue: { type: Number, default: 0 },
  minDate: { type: String, default: '01.01.2000' },
  maxValue: { type: Number, default: 1 },
  maxDate: { type: String, default: '01.01.2000' },
})

const card = ref()
const cardHovered = useElementHover(card)
const detailsOpen = ref(props.open)
const cardData = dashboardStore.data[props.id]

const detailsHeight = () => {
  if (detailsOpen.value) {
    return 'opacity-100 p-4 max-h-[35rem]'
  } else if (cardHovered.value) {
    return 'opacity-0 max-h-0 p-2'
  } else {
    return 'opacity-0 max-h-0 p-0'
  }
}

watch(detailsOpen, (newValue) => {
  if (newValue) {
    dashboardStore.detailedUpdate(props.id)
  }
})
</script>

<template>
  <div class="m-2 flex w-64 flex-col overflow-hidden rounded-xl bg-gray-50 shadow">
    <!-- card header -->
    <div
      ref="card"
      class="z-10 cursor-pointer select-none bg-white p-3"
      @click="detailsOpen = !detailsOpen"
    >
      <p class="mb-2 text-xl text-gray-800">{{ title }}</p>
      <p class="text-right text-5xl font-semibold text-teal-500">
        {{ cardData.value }}<span class="text-4xl">{{ unit }}</span>
      </p>
    </div>

    <!-- card details -->
    <div
      class="transition-card-body overflow-hidden border-gray-50 duration-300 ease-in-out"
      :class="detailsHeight()"
    >
      <slot>
        <HighscoreBar
          :min-value="cardData.min.value"
          :min-date="cardData.min.date"
          :max-value="cardData.max.value"
          :max-date="cardData.max.date"
          :current-value="cardData.value"
          :unit="unit"
        />

        <SparklineChart :series-name="title" :series-data="cardData.liveData" :unit="unit" />

        <div class="grid grid-cols-2 pt-3 text-gray-700">
          <p>Ø Vortag</p>
          <p class="text-right text-lg font-semibold">{{ cardData.avg.yesterday }} {{ unit }}</p>
          <p>Ø 7 Tage</p>
          <p class="text-right text-lg font-semibold">{{ cardData.avg.lastWeek }} {{ unit }}</p>
        </div>

        <slot name="details"></slot>
      </slot>
    </div>
  </div>
</template>
