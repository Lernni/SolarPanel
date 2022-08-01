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
    class="nav-item text-md ml-3 mt-3 text-gray-600 transition-all"
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

<style scoped lang="scss">
.nav-item {
  .active,
  &:hover {
    @apply font-bold text-blue-600;
  }
}
</style>
