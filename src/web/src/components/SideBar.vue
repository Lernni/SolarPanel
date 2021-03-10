<template>
  <div class="bg-light h-100">
    <div class="nav flex-lg-column nav-pills bg-light" id="v-pills-tab" role="tablist" aria-orientation="vertical">
      <router-link v-for="(r,i) in routes" :key="i" :route="r" :to=r.path class="nav-link" data-toggle="pill" role="tab" aria-selected="true">
        {{r.name}}
      </router-link>
    </div>
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

<style scoped>

  .nav {
    width: max-content;
    margin-left: auto;
    margin-right: auto;
  }

  @media (min-width: 992px) {
    .nav {
      height: 100%;
      width: 100%;
    }
  }

</style>