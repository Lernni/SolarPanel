<script setup>
import { ArrowRightIcon } from '@heroicons/vue/24/solid'

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
  <div class="h-8 w-8 rounded-md bg-gray-200">
    <ArrowRightIcon
      class="h-full w-full p-1.5 transition-transform duration-500"
      :style="{ transform: 'rotate(' + -getPercentageValue() * 0.9 + 'deg)' }"
    />
  </div>
</template>
