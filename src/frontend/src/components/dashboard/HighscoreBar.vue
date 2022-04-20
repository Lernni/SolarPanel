<script setup>
import { ref, watch, onMounted } from 'vue';
import { useElementHover } from '@vueuse/core'
import noUiSlider from 'nouislider';
import 'nouislider/dist/nouislider.css';

const props = defineProps({
  minValue: String,
  minDate: String,
  maxValue: String,
  maxDate: String,
  currentValue: String,
  unit: String,
})

const highscoreBar = ref()

onMounted(() => {
  noUiSlider.create(highscoreBar.value, {
    range: {
        'min': parseFloat(props.minValue),
        'max': parseFloat(props.maxValue)
    },
    start: [parseFloat(props.minValue), parseFloat(props.currentValue), parseFloat(props.maxValue) ],
    tooltips: [{
      to: (value) => {
        return value + ' ' + props.unit + '<span class="tooltip-info"> - ' + props.minDate + '</span>'
      }
    },
    {
      to: (value) => {
        return value + ' ' + props.unit
      }
    },
    {
      to: (value) => {
        return '<span class="tooltip-info">' + props.maxDate + ' - </span>' + value + ' ' + props.unit
      }
    }]
  })

  let origins = highscoreBar.value.getElementsByClassName('noUi-origin');
  origins[0].id = 'first-thumb';
  origins[1].id = 'middle-thumb';
  origins[2].id = 'last-thumb';

  const firstHandle = ref(origins[0].getElementsByClassName('noUi-handle')[0])
  const lastHandle = ref(origins[2].getElementsByClassName('noUi-handle')[0])

  const firstTooltip = ref(origins[0].getElementsByClassName('noUi-tooltip')[0])
  const lastTooltip = ref(origins[2].getElementsByClassName('noUi-tooltip')[0])

  const firstTooltipHovered = useElementHover(firstHandle);
  const lastTooltipHovered = useElementHover(lastHandle);

  watch(firstTooltipHovered, (value) => {
    if (value) {
      lastTooltip.value.style.opacity = '0'
    } else {
      lastTooltip.value.style.opacity = '100%'
    }
  })

  watch(lastTooltipHovered, (value) => {
    if (value) {
      firstTooltip.value.style.opacity = '0'
    } else {
      firstTooltip.value.style.opacity = '100%'
    }
  })

  watch(props, (newProps) => {
    console.log(newProps)
    highscoreBar.value.noUiSlider.updateOptions({
      range: {
        'min': parseFloat(newProps.minValue),
        'max': parseFloat(newProps.maxValue)
      }
    })
    highscoreBar.value.noUiSlider.set([parseFloat(newProps.minValue), parseFloat(newProps.currentValue), parseFloat(newProps.maxValue)])
  })
})

</script>

<template>
  <div class="px-6 my-10 border-inherit">
    <div disabled id="highscore-bar" ref="highscoreBar" class="w-full h-full"></div>
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