<template>
  <NavBar title="SolarPanel"/>
  <div class="row no-gutters">
    <div class="col-md-2">
      <SideBar/>
    </div>
    <div class="col-md-10">
      <router-view/>
    </div>
  </div>
</template>

# <router-link to="/about">About</router-link>

<script>
import SideBar from './components/SideBar.vue'
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components : {
    SideBar,
    NavBar
  }
}
</script>

<style lang="scss">
  .no-gutters {
    margin-right: 0;
    margin-left: 0;

    > .col,
    > [class*="col-"] {
      padding-right: 0;
      padding-left: 0;
    }
  }
</style>
