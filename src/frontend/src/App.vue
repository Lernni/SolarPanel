<template>
  <b-container fluid class="p-0">
    <b-row no-gutters>
      <b-col id="header">
        <NavBar title="SolarPanel"/>
      </b-col>
    </b-row>
    <b-row id="content" no-gutters>
      <b-col md="auto" v-show="isLoggedIn" id="sidebar-column">
        <SideBar/>
      </b-col>
      <b-col id="router-view">
        <b-container :fluid="$screen.sm">
          <router-view/>
        </b-container>
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
  /* */
</style>