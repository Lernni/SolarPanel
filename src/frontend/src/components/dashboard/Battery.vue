<script setup>
defineProps({
  value: { type: Number, default: 0 },
  diffDay: { type: Number, default: 0 },
  diffWeek: { type: Number, default: 0 },
})
</script>

<template>
  <div class="flex h-60 w-24 flex-col items-center">
    <div class="h-2 w-10 rounded-t-lg bg-gray-200"></div>
    <div class="h-full w-full rounded-xl border-4 border-gray-200">
      <div
        class="relative flex h-full w-full items-center justify-center overflow-hidden rounded-xl border-4 border-gray-50 bg-gray-200"
      >
        <p class="z-10 text-3xl font-semibold">{{ value }}<span class="text-base">%</span></p>
        <div
          class="absolute bottom-0 w-full rounded-md bg-green-400 transition-[height] duration-500 ease-in-out"
          :style="{ height: value + '%' }"
          role="progressbar"
          :aria-valuenow="value"
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
