<template>
  <div>
    <ul v-if="$route.name === 'Messwerte'" class="nav flex-column">
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <database-icon class="tab-icon"></database-icon> -->
        <div class="tab-title">Benutzerdefiniert</div>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <database-icon class="tab-icon"></database-icon> -->
        <div class="tab-title">Letzte Stunde</div>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <database-icon class="tab-icon"></database-icon> -->
        <div class="tab-title">Letzter Tag</div>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <database-icon class="tab-icon"></database-icon> -->
        <div class="tab-title">Letzte Woche</div>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <database-icon class="tab-icon"></database-icon> -->
        <div class="tab-title">Letzter Monat</div>
      </router-link>
      <router-link class="nav-link" :to="{ name: 'Browser' }">
        <!-- <log-out-icon class="tab-icon"></log-out-icon> -->
        <div class="tab-title">Messwerte exportieren</div>
      </router-link>
    </ul>

    <router-view/>
  </div>
</template>

<script>

export default {
  name: 'Stats'
}
</script>