<template>
<div id="sidebar-box">
  <div id="sidebar" class="bg-light">
    <b-nav :vertical="$screen.md && $screen.width != 800" pills>
      <b-nav-item :to="{ name: 'dashboard' }" exact exact-active-class="active">
        <b-icon icon="brightness-high-fill"></b-icon>
        <div v-if="device == 'External'" class="d-none d-sm-inline">Dashboard</div>
      </b-nav-item>
      <b-nav-item v-if="device == 'External'" :to="{ name: 'browser' }" exact exact-active-class="active">
        <b-icon icon="bar-chart-fill"></b-icon>
        <div class="d-none d-sm-inline">Messwerte</div>
      </b-nav-item>
      <b-nav-item :to="{ name: 'settings' }" exact exact-active-class="active">
        <b-icon icon="sliders"></b-icon>
        <div v-if="device == 'External'" class="d-none d-sm-inline">Einstellungen</div>
      </b-nav-item>
    </b-nav>
  </div>
</div>
</template>

<script>
export default {
  name: 'SideBar',
  computed: {
    device() {
      return this.$store.state.device
    }
  }
}
</script>