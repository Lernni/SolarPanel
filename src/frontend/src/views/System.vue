<template>
  <div>
    <ul v-if="$route.name === 'System'" class="nav flex-column">
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <sliders-icon class="tab-icon"></sliders-icon> -->
        <div class="tab-title">Shuntwerte bearbeiten</div>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <sliders-icon class="tab-icon"></sliders-icon> -->
        <div class="tab-title">Highscore zurücksetzen</div>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <sliders-icon class="tab-icon"></sliders-icon> -->
        <div class="tab-title">System herunterfahren</div>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <bell-icon class="tab-icon"></bell-icon> -->
        <div class="tab-title">Ereignisse der letzten Woche</div>
      </router-link>
    </ul>

    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'System'
}
</script>