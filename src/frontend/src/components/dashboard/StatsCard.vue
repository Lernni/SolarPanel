<script setup>
import HighscoreBar from '@/components/dashboard/HighscoreBar.vue';

import { ref } from 'vue'
import { useElementHover } from '@vueuse/core'

defineProps({
  title: String,
  value: String,
  unit: String,

  minValue: String,
  minDate: String,
  maxValue: String,
  maxDate: String,
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
  <div class="m-2 rounded-xl overflow-hidden flex flex-col w-64 shadow bg-gray-50">
    <!-- card header -->
    <div
      @click="detailsOpen = !detailsOpen"
      ref="card"
      class="bg-white p-3 z-10 cursor-pointer select-none"
    >
      <p class="text-xl mb-2 text-gray-800">{{ title }}</p>
      <p class="text-right text-5xl font-semibold text-teal-500">
        {{ value }}<span class="text-4xl">{{ unit }}</span>
      </p>
    </div>

    <!-- card details -->
    <div
      class="transition-card-body duration-300 ease-in-out border-gray-50 overflow-hidden"
      :class="detailsHeight()"
    >
      <slot>
        <HighscoreBar minValue="10.7" minDate="19" maxValue="15.8" :currentValue="value" :unit="unit" />
        <div class="text-gray-700 grid grid-cols-2 pt-3">
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