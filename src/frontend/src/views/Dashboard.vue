<script setup>
import StatsCard from '@/components/dashboard/StatsCard.vue'
import Battery from '@/components/dashboard/Battery.vue'
import ArrowIndicator from '@/components/dashboard/ArrowIndicator.vue'

import { useDashboardStore } from '@/stores/dashboard'

const dashboardStore = useDashboardStore()

setInterval(() => {
  dashboardStore.update()
}, 1000)
</script>

<template>
  <div class="mt-3 gap-0 sm:columns-2 xl:flex xl:items-start xl:flex-wrap justify-center">
    <StatsCard id="battery" open title="Akkustatus" unit="%">
      <div class="flex justify-between">
        <Battery :value="dashboardStore.data.battery.value" diff-day="30" />
        <div class="flex w-32 flex-col">
          <div
            class="relative flex h-full flex-auto snap-x snap-mandatory overflow-hidden scroll-smooth"
          >
            <div class="absolute flex">
              <div id="slide-1" class="slide">
                <div>
                  <p class="text-gray-700">Ladezustand</p>
                  <p class="text-2xl font-semibold">
                    {{ dashboardStore.data.battery.soc }} <span class="text-lg">Ah</span>
                  </p>
                  <ArrowIndicator
                    :value="dashboardStore.data.battery.gain.value"
                    :min="dashboardStore.data.battery.gain.min"
                    :max="dashboardStore.data.battery.gain.max"
                  />
                </div>
                <div>
                  <p class="text-gray-700">Kapazität</p>
                  <p class="text-2xl font-semibold">
                    {{ dashboardStore.data.battery.capacity }} <span class="text-lg">Ah</span>
                  </p>
                </div>
              </div>
              <!-- <div id="slide-2" class="slide">
                <div>
                  <p class="text-gray-700">Ladezustand</p>
                  <p class="text-2xl font-semibold">100.44 <span class="text-lg">Ah</span></p>
                  <ArrowIndicator state=80 />
                </div>
                <div>
                  <p class="text-gray-700">Kapazität</p>
                  <p class="text-2xl font-semibold">100.2 <span class="text-lg">Ah</span></p>
                </div>
              </div> -->
            </div>
          </div>
          <!-- <div class="space-x-2 w-full text-center slide-controls">
            <input
              type="radio"
              name="slide-control"
              class="slide-control"
              onclick="location.href='#slide-1'"
            />
            <input
              type="radio"
              name="slide-control"
              class="slide-control"
              onclick="location.href='#slide-2'"
            />
          </div> -->
        </div>
      </div>
    </StatsCard>
    <StatsCard id="voltage" title="Spannung" unit="V" />
    <StatsCard id="input_current" title="Eingangsstrom" unit="A">
      <template #details>
        <div class="pt-3">
          <p class="text-gray-700">Eingangsleistung</p>
          <p class="text-2xl font-semibold">
            {{ dashboardStore.data.inputPower }} <span class="text-lg">W</span>
          </p>
        </div>
      </template>
    </StatsCard>
    <StatsCard id="output_current" title="Ausgangsstrom" unit="A">
      <template #details>
        <div class="pt-3">
          <p class="text-gray-700">Ausgangsleistung</p>
          <p class="text-2xl font-semibold">
            {{ dashboardStore.data.outputPower }} <span class="text-lg">W</span>
          </p>
        </div>
      </template>
    </StatsCard>
  </div>
</template>

<style lang="scss">
// .slide-controls .slide-control[type='radio'] {
//   @apply bg-gray-200 text-gray-200 border-none cursor-pointer;
//   @apply h-3 w-3 transition-[background-color] rounded-full;
//   -webkit-appearance: none;
//   -moz-appearance: none;
//   --tw-ring-color: none;

//   &:hover,
//   &:checked {
//     @apply bg-gray-300;
//   }
// }

// .slide {
//   @apply flex flex-col space-y-4 w-max snap-start transition-transform duration-500;
//   transform: scale(1);
//   transform-origin: center center;
// }
</style>
