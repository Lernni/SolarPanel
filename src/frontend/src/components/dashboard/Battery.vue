<script setup>
defineProps({
  soc: { type: Number, default: 0 },
  diffDay: { type: Number, default: 0 },
  diffWeek: { type: Number, default: 0 },
})
</script>

<template>
  <div class="flex flex-col items-center w-24 h-60">
    <div class="w-10 h-2 bg-gray-200 rounded-t-lg"></div>
    <div class="w-full h-full rounded-xl border-4 border-gray-200">
      <div
        class="flex overflow-hidden relative justify-center items-center w-full h-full bg-gray-200 rounded-xl border-4 border-gray-50"
      >
        <p class="z-10 text-3xl font-semibold">{{ soc }}<span class="text-base">%</span></p>
        <div
          class="absolute bottom-0 w-full bg-green-400 rounded-md transition-[height] duration-500 ease-in-out"
          :style="{ height: soc + '%' }"
          role="progressbar"
          :aria-valuenow="soc"
          aria-valuemin="0"
          aria-valuemax="100"
        >
          <!-- <div
            class="flex w-full bg-gray-50/30"
            :style="{ height: diffDay + '%' }"
          >
          </div> -->
        </div>
      </div>
    </div>
  </div>
</template>
