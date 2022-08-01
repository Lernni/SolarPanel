<script setup>
import { ref, watch, onMounted } from 'vue'
import { useElementHover } from '@vueuse/core'
import noUiSlider from 'nouislider'
import 'nouislider/dist/nouislider.css'

const props = defineProps({
  minValue: { type: Number, default: 0 },
  minDate: { type: String, default: '01.01.2000' },
  maxValue: { type: Number, default: 1 },
  maxDate: { type: String, default: '01.01.2000' },
  currentValue: { type: Number, default: 0 },
  unit: { type: String, default: '-' },
})

const highscoreBar = ref()

const firstTooltipHoveredState = ref(false)
const lastTooltipHoveredState = ref(false)

const firstTooltipOpacity = () => {
  return firstTooltipHoveredState.value ? 0 : 1
}

const lastTooltipOpacity = () => {
  return lastTooltipHoveredState.value ? 0 : 1
}

onMounted(() => {
  noUiSlider.create(highscoreBar.value, {
    range: {
      min: props.minValue,
      max: props.maxValue,
    },
    start: [props.minValue, props.currentValue, props.maxValue],
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
          return value.toFixed(1) + ' ' + props.unit
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

  const firstTooltipHovered = useElementHover(firstHandle)
  const lastTooltipHovered = useElementHover(lastHandle)

  watch(props, (newProps) => {
    highscoreBar.value.noUiSlider.updateOptions({
      range: {
        min: newProps.minValue,
        max: newProps.maxValue,
      },
    })
    highscoreBar.value.noUiSlider.set([newProps.minValue, newProps.currentValue, newProps.maxValue])
  })

  watch(firstTooltipHovered, (newValue) => {
    lastTooltipHoveredState.value = newValue
  })

  watch(lastTooltipHovered, (newValue) => {
    firstTooltipHoveredState.value = newValue
  })
})
</script>

<template>
  <div class="my-10 border-inherit px-6">
    <div id="highscore-bar" ref="highscoreBar" disabled class="h-full w-full"></div>
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

  #first-thumb .noUi-tooltip {
    opacity: v-bind(firstTooltipOpacity());

    .tooltip-info {
      @apply left-full;
    }
  }

  #last-thumb .noUi-tooltip {
    opacity: v-bind(lastTooltipOpacity());

    .tooltip-info {
      @apply right-full;
    }
  }
}
</style>
