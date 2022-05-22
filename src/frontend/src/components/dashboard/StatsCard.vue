<script setup>
import HighscoreBar from './HighscoreBar.vue'
import { ref, watch } from 'vue'
import { useElementHover } from '@vueuse/core'
import { useDashboardStore } from '@/stores/dashboard'

const dashboardStore = useDashboardStore()

const props = defineProps({
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
const detailsOpen = ref(false)
const cardData = dashboardStore.data[props.id]

const detailsHeight = () => {
  if (detailsOpen.value) {
    return 'opacity-100 max-h-72 p-4'
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
  <div class="flex overflow-hidden flex-col m-2 w-64 bg-gray-50 rounded-xl shadow">
    <!-- card header -->
    <div
      ref="card"
      class="z-10 p-3 bg-white cursor-pointer select-none"
      @click="detailsOpen = !detailsOpen"
    >
      <p class="mb-2 text-xl text-gray-800">{{ title }}</p>
      <p class="text-5xl font-semibold text-right text-teal-500">
        {{ cardData.value }}<span class="text-4xl">{{ unit }}</span>
      </p>
    </div>

    <!-- card details -->
    <div
      class="overflow-hidden border-gray-50 duration-300 ease-in-out transition-card-body"
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
        <div class="grid grid-cols-2 pt-3 text-gray-700">
          <p>Ø Vortag</p>
          <p class="text-lg font-semibold text-right">{{ cardData.avg.yesterday }} {{ unit }}</p>
          <p>Ø 7 Tage</p>
          <p class="text-lg font-semibold text-right">{{ cardData.avg.lastWeek }} {{ unit }}</p>
        </div>
        <slot name="details"></slot>
      </slot>
    </div>
  </div>
</template>
