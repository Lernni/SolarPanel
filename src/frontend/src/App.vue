<template>
  <b-container fluid class="h-100 p-0">
    <b-row no-gutters class="h-100">
      <b-col lg="auto">
        <SideBar/>
      </b-col>
      <b-col>
        <NavBar title="SolarPanel"/>
        <router-view/>
      </b-col>
    </b-row>
  </b-container>

  <!--<div>
    <NavBar title="SolarPanel"/>
    <div class="h-100">
      <b-row align-v="stretch">
        <b-col lg="auto" class="order-lg-1 order-sm-2">
          <SideBar/>
        </b-col>
        <b-col class="order-lg-2 order-sm-1">
          <router-view/>
        </b-col>
      </b-row>
    </div>
  </div>-->
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

  .nav-link {
    font-size: 25px;
  }

  .tab-title {
    display: inline;
    padding-left: 5px;
    vertical-align: middle;
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
