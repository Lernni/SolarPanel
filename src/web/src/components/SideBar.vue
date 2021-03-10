<template>
  <div class="nav flex-column nav-pills" id="v-pills-tab" role="tablist" aria-orientation="vertical">
    <router-link v-for="(r,i) in routes" :key="i" :route="r" :to=r.path class="nav-link" data-toggle="pill" role="tab" aria-selected="true">
      {{r.name}}
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'SideBar',
  computed: {
    routes() {
      return this.$router.options.routes
    }
  }
}
</script>

<style>

</style>