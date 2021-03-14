<template>
  <div class="wrapper h-100">
    <NavBar title="SolarPanel"/>
    <div class="row no-gutters h-100">
      <div class="sidebar col-lg-auto order-lg-1 order-sm-2">
        <SideBar/>
      </div>
      <div class="content col-lg order-lg-2 order-sm-1">
        <router-view/>
      </div>
    </div>
  </div>
</template>

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
  html, body, #app {
    height: 100%;
    user-select: none;
  }

  .content {
    height: 90%;
    padding: 15px !important;
  }

  @media (min-width: 992px) {
    html, body, #app {
      user-select: auto;
    }

    .content {
      height: 100%
    }
  }

</style>
