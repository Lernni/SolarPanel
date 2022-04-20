<script setup>
import { ArrowRightIcon } from '@heroicons/vue/solid'

defineProps({
  state: Number
})
</script>

<template>
  <div class="w-8 h-8 rounded-md bg-gray-200">
    <ArrowRightIcon
      class="h-full w-full p-1.5 transition-transform duration-500"
      :style="{ transform: 'rotate(' + (-state * 0.9) + 'deg)' }"
    />
  </div>
</template>