<template>
  <div class="wrapper overflow-hidden h-100">
    <NavBar title="SolarPanel"/>
    <div class="row no-gutters h-100">
      <div class="sidebar col-lg-1 order-lg-1 order-sm-2">
        <SideBar/>
      </div>
      <div class="content col-lg-11 order-lg-2 order-sm-1">
        <router-view/>
      </div>
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

  html, body, #app {
    height: 100%;
  }

  .content {
    height: 90%
  }

  @media (min-width: 992px) {
    .content {

    }
  }

</style>
