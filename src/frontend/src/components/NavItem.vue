<script setup>
import * as heroIcons from '@heroicons/vue/24/solid'

const props = defineProps({
  title: { type: String, default: 'Title' },
  path: { type: String, default: '/' },
  icon: { type: String, default: 'HomeIcon' },
})
</script>

<template>
  <div>
    <a :href="props.path" class="transition-color">
      <component :is="heroIcons[props.icon]" class="inline h-6 w-6" />
      <span class="ml-2 hidden align-middle transition-all sm:inline-block" :title="props.title">{{
        props.title
      }}</span>
    </a>
  </div>
</template>

<style scoped lang="scss">
.active,
:hover {
  @apply font-bold text-blue-600;
}

span::before {
  @apply block h-0 font-bold overflow-hidden invisible;
  content: attr(title);
}
</style>
