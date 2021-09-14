<template>
  <b-container fluid class="h-100 p-0">
    <b-row no-gutters class="h-100">
      <b-col lg="auto" v-show="isLoggedIn">
        <SideBar/>
      </b-col>
      <b-col>
        <NavBar title="SolarPanel"/>
        <router-view/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import SideBar from './components/SideBar.vue'
import NavBar from './components/NavBar.vue'

export default {
  name: 'App',
  components : {
    SideBar,
    NavBar
  },

  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn
    }
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

  /*.nav-link {
    font-size: 25px;
  }*/

  /*.tab-title {
    display: inline;
    padding-left: 5px;
    vertical-align: middle;
  }*/

  @media (min-width: 992px) {
    html, body, #app {
      user-select: auto;
    }

    .content {
      height: 100%
    }
  }

</style>
