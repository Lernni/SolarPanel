<script setup>
import * as heroIcons from '@heroicons/vue/solid'

const props = defineProps({
  title: { type: String, default: 'Title' },
  path: { type: String, default: '/' },
  icon: { type: String, default: 'HomeIcon' },
})
</script>

<template>
  <div>
    <a :href="props.path">
      <component :is="heroIcons[props.icon]" class="inline h-6 w-6" />
      <span class="ml-2 align-middle">{{ props.title }}</span>
    </a>
  </div>
</template>
