<script setup>
import StatsCard from '@/components/dashboard/StatsCard.vue'
import Battery from '@/components/dashboard/Battery.vue'
import ArrowIndicator from '@/components/dashboard/ArrowIndicator.vue'
</script>

<template>
  <div class="flex items-start">
    <StatsCard title="Akkustatus" value="35" unit="%">
      <div class="flex justify-between">
        <Battery soc="95" diff-day="30" />
        <div class="flex flex-col w-28">
          <div
            class="flex overflow-hidden relative flex-auto h-full scroll-smooth snap-x snap-mandatory"
          >
            <div class="flex absolute">
              <div id="slide-1" class="slide">
                <div>
                  <p class="text-gray-700">Ladezustand</p>
                  <p class="text-2xl font-semibold">100.44 <span class="text-lg">Ah</span></p>
                  <ArrowIndicator state="0" />
                </div>
                <div>
                  <p class="text-gray-700">Kapazität</p>
                  <p class="text-2xl font-semibold">100.2 <span class="text-lg">Ah</span></p>
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
          <div class="space-x-2 w-full text-center slide-controls">
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
          </div>
        </div>
      </div>
    </StatsCard>
    <StatsCard title="Spannung" value="13.5" unit="V" />
    <StatsCard title="Eingangsstrom" value="6.4" unit="A">
      <template #details>
        <div class="pt-3">
          <p class="text-gray-700">Eingangsleistung</p>
          <p class="text-2xl font-semibold">26 <span class="text-lg">W</span></p>
        </div>
      </template>
    </StatsCard>
    <StatsCard title="Ausgangsstrom" value="12.2" unit="A">
      <template #details>
        <div class="pt-3">
          <p class="text-gray-700">Ausgangsleistung</p>
          <p class="text-2xl font-semibold">78 <span class="text-lg">W</span></p>
        </div>
      </template>
    </StatsCard>
  </div>
</template>

<style lang="scss">
.slide-controls .slide-control[type='radio'] {
  @apply bg-gray-200 text-gray-200 border-none cursor-pointer;
  @apply h-3 w-3 transition-[background-color] rounded-full;
  -webkit-appearance: none;
  -moz-appearance: none;
  --tw-ring-color: none;

  &:hover,
  &:checked {
    @apply bg-gray-300;
  }
}

.slide {
  @apply flex flex-col space-y-4 w-max snap-start transition-transform duration-500;
  transform: scale(1);
  transform-origin: center center;
}
</style>
