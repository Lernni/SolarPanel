<script setup>
import NavItem from './NavItem.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const routes = router.options.routes.filter(({ meta: { showItem } }) => showItem)
</script>

<template>
  <div
    v-for="route in routes"
    :key="route.path"
    class="text-md m-3 mr-5 px-3 text-gray-600 sm:px-0"
  >
    <NavItem
      :title="route.meta.title"
      :path="route.path"
      :icon="route.meta.icon"
      class="mb-2"
      :class="$route.path == route.path ? 'active' : ''"
    />
  </div>
</template>
