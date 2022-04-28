<script setup>
import { ArrowRightIcon } from '@heroicons/vue/solid'

defineProps({
  state: {
    type: Number,
    default: 0,
  },
})
</script>

<template>
  <div class="w-8 h-8 bg-gray-200 rounded-md">
    <ArrowRightIcon
      class="p-1.5 w-full h-full transition-transform duration-500"
      :style="{ transform: 'rotate(' + -state * 0.9 + 'deg)' }"
    />
  </div>
</template>
