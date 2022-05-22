<script setup>
import { ArrowRightIcon } from '@heroicons/vue/solid'

const props = defineProps({
  value: {
    type: Number,
    default: 0,
  },
  max: {
    type: Number,
    default: 0,
  },
  min: {
    type: Number,
    default: 0,
  },
})

const getPercentageValue = () => {
  if (props.value > 0) {
    return (props.value / props.max) * 100
  } else {
    return (props.value / props.min) * 100
  }
}
</script>

<template>
  <div class="w-8 h-8 bg-gray-200 rounded-md">
    <ArrowRightIcon
      class="p-1.5 w-full h-full transition-transform duration-500"
      :style="{ transform: 'rotate(' + -getPercentageValue() * 0.9 + 'deg)' }"
    />
  </div>
</template>
