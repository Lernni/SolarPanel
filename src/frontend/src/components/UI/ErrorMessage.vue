<script setup>
import { ExclamationCircleIcon } from '@heroicons/vue/outline'
</script>

<template>
  <div class="my-1 text-red-600">
    <ExclamationCircleIcon class="inline h-6 w-6" />
    <span class="ml-1 align-middle">
      <slot></slot>
    </span>
  </div>
</template>
