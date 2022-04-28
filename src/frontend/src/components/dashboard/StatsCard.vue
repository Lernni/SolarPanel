<script setup>
import HighscoreBar from './HighscoreBar.vue'
import { ref } from 'vue'
import { useElementHover } from '@vueuse/core'

defineProps({
  title: { type: String, default: 'Title' },
  value: { type: String, default: '0.0' },
  unit: { type: String, default: '-' },

  minValue: { type: String, default: '0' },
  minDate: { type: String, default: '01.01.2000' },
  maxValue: { type: String, default: '1' },
  maxDate: { type: String, default: '01.01.2000' },
})

const card = ref()
const cardHovered = useElementHover(card)
const detailsOpen = ref(false)

const detailsHeight = () => {
  if (detailsOpen.value) {
    return 'opacity-100 max-h-72 p-4'
  } else if (cardHovered.value) {
    return 'opacity-0 max-h-0 p-2'
  } else {
    return 'opacity-0 max-h-0 p-0'
  }
}
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
        {{ value }}<span class="text-4xl">{{ unit }}</span>
      </p>
    </div>

    <!-- card details -->
    <div
      class="overflow-hidden border-gray-50 duration-300 ease-in-out transition-card-body"
      :class="detailsHeight()"
    >
      <slot>
        <HighscoreBar
          min-value="10.7"
          min-date="19"
          max-value="15.8"
          :current-value="value"
          :unit="unit"
        />
        <div class="grid grid-cols-2 pt-3 text-gray-700">
          <p>Ø Vortag</p>
          <p class="text-lg font-semibold text-right">13.23 {{ unit }}</p>
          <p>Ø 7 Tage</p>
          <p class="text-lg font-semibold text-right">13.15 {{ unit }}</p>
        </div>
        <slot name="details"></slot>
      </slot>
    </div>
  </div>
</template>
