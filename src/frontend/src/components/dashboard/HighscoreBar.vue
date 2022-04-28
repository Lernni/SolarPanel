<script setup>
import { ref, watch, onMounted } from 'vue'
import { useElementHover } from '@vueuse/core'
import noUiSlider from 'nouislider'
import 'nouislider/dist/nouislider.css'

const props = defineProps({
  minValue: { type: String, default: '0' },
  minDate: { type: String, default: '01.01.2000' },
  maxValue: { type: String, default: '1' },
  maxDate: { type: String, default: '01.01.2000' },
  currentValue: { type: String, default: '0' },
  unit: { type: String, default: '-' },
})

const highscoreBar = ref()

onMounted(() => {
  noUiSlider.create(highscoreBar.value, {
    range: {
      min: Number.parseFloat(props.minValue),
      max: Number.parseFloat(props.maxValue),
    },
    start: [
      Number.parseFloat(props.minValue),
      Number.parseFloat(props.currentValue),
      Number.parseFloat(props.maxValue),
    ],
    tooltips: [
      {
        to: (value) => {
          return (
            value + ' ' + props.unit + '<span class="tooltip-info"> - ' + props.minDate + '</span>'
          )
        },
      },
      {
        to: (value) => {
          return value + ' ' + props.unit
        },
      },
      {
        to: (value) => {
          return (
            '<span class="tooltip-info">' + props.maxDate + ' - </span>' + value + ' ' + props.unit
          )
        },
      },
    ],
  })

  let origins = highscoreBar.value.querySelectorAll('.noUi-origin')
  origins[0].id = 'first-thumb'
  origins[1].id = 'middle-thumb'
  origins[2].id = 'last-thumb'

  const firstHandle = ref(origins[0].querySelectorAll('.noUi-handle')[0])
  const lastHandle = ref(origins[2].querySelectorAll('.noUi-handle')[0])

  const firstTooltip = ref(origins[0].querySelectorAll('.noUi-tooltip')[0])
  const lastTooltip = ref(origins[2].querySelectorAll('.noUi-tooltip')[0])

  const firstTooltipHovered = useElementHover(firstHandle)
  const lastTooltipHovered = useElementHover(lastHandle)

  watch(firstTooltipHovered, (value) => {
    lastTooltip.value.style.opacity = value ? '0' : '100%'
  })

  watch(lastTooltipHovered, (value) => {
    firstTooltip.value.style.opacity = value ? '0' : '100%'
  })

  watch(props, (newProps) => {
    console.log(newProps)
    highscoreBar.value.noUiSlider.updateOptions({
      range: {
        min: Number.parseFloat(newProps.minValue),
        max: Number.parseFloat(newProps.maxValue),
      },
    })
    highscoreBar.value.noUiSlider.set([
      Number.parseFloat(newProps.minValue),
      Number.parseFloat(newProps.currentValue),
      Number.parseFloat(newProps.maxValue),
    ])
  })
})
</script>

<template>
  <div class="px-6 my-10 border-inherit">
    <div id="highscore-bar" ref="highscoreBar" disabled class="w-full h-full"></div>
  </div>
</template>

<style lang="scss">
#highscore-bar {
  @apply bg-teal-500 border-none border-inherit h-2;

  .noUi-origin,
  .noUi-base,
  .noUi-handle {
    @apply bg-inherit border-inherit;
  }

  .noUi-connects,
  .noUi-handle {
    @apply cursor-default;
  }

  .noUi-handle {
    @apply w-6 h-6;
    @apply rounded-full border-4 shadow-none;
    @apply -top-2 -right-3;

    &:before,
    &:after {
      @apply hidden;
    }
  }

  .noUi-tooltip {
    @apply border-none bg-transparent;

    .highscore-info {
      @apply text-gray-500;
    }
  }

  #middle-thumb .noUi-handle .noUi-tooltip {
    @apply top-[120%] h-max;
  }

  #first-thumb,
  #last-thumb {
    .noUi-handle {
      @apply cursor-pointer;

      &:hover .noUi-tooltip .tooltip-info {
        @apply opacity-100;
      }

      .noUi-tooltip .tooltip-info {
        @apply absolute pointer-events-none;
        @apply text-gray-600 bg-inherit;
        @apply transition-opacity opacity-0;
      }
    }
  }

  #first-thumb .noUi-tooltip .tooltip-info {
    @apply left-full;
  }

  #last-thumb .noUi-tooltip .tooltip-info {
    @apply right-full;
  }
}
</style>
