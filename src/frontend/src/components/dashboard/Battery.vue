<script setup>

defineProps({
  soc: Number,
  diffDay: Number,
  diffWeek: Number,
})
</script>

<template>
  <div class="flex flex-col items-center w-24 h-60">
    <div class="bg-gray-200 w-10 h-2 rounded-t-lg"></div>
    <div class="border-4 w-full h-full border-gray-200 rounded-xl">
      <div class="flex relative w-full h-full border-4 border-gray-50 bg-gray-200 rounded-xl justify-center items-center overflow-hidden">
        <p class="z-10 text-3xl font-semibold">{{ soc }}<span class="text-base">%</span></p>
        <div
          class="absolute w-full bottom-0 bg-green-400 rounded-md transition-[height] duration-500 ease-in-out"
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