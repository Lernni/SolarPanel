<template>
  <b-container fluid class="h-100 p-0">
    <b-row no-gutters>
      <b-col id="header" class="position-fixed">
        <NavBar title="SolarPanel"/>
      </b-col>
    </b-row>
    <b-row id="content" no-gutters align-v="stretch" class="w-100">
      <b-col lg="auto" v-show="isLoggedIn" class="h-100 position-fixed">
        <SideBar/>
      </b-col>
      <b-col id="router-view" :class="isLoggedIn ? '' : 'm-3'">
        <router-view/>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import SideBar from './components/SideBar.vue'
import NavBar from './components/NavBar.vue'
import Screensaver from './scripts/screensaver'

export default {
  name: 'App',
  components : {
    SideBar,
    NavBar
  },

  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn
    },

    device() {
      return this.$store.state.device
    }
  },

  watch: {
    device: function() {
      if (this.device == 'Internal') {
        Screensaver()
      }
    }
  }
}
</script>

<style lang="scss">
  // html, body, #app {
  //   height: 100%;
  //   user-select: none;
  // }

  /*.nav-link {
    font-size: 25px;
  }*/

  /*.tab-title {
    display: inline;
    padding-left: 5px;
    vertical-align: middle;
  }*/

</style>
