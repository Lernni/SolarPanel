<template>
  <div class="navbar nav-box bg-light h-100">
    <nav class="nav flex-lg-column nav-pills bg-light" role="tablist">
      <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Dashboard' }">
        <sun-icon class="tab-icon"></sun-icon>
        <div class="tab-title">Dashboard</div>
      </router-link>
      <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Messwerte' }">
        <activity-icon class="tab-icon"></activity-icon>
        <div class="tab-title">Messwerte</div>
      </router-link>
      <nav class="nav nav-pills flex-lg-column" role="tablist">
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Browser' }">
          <database-icon class="tab-icon"></database-icon>
          <div class="tab-title">Browser</div>
        </router-link>
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Export' }">
          <log-out-icon class="tab-icon"></log-out-icon>
          <div class="tab-title">Export</div>
        </router-link>
      </nav>
      <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'System' }">
        <sliders-icon class="tab-icon"></sliders-icon>
        <div class="tab-title">System</div>
      </router-link>
      <nav class="nav nav-pills flex-lg-column" role="tablist">
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Einstellungen' }">
          <sliders-icon class="tab-icon"></sliders-icon>
          <div class="tab-title">Einstellungen</div>
        </router-link>
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Ereignisse' }">
          <bell-icon class="tab-icon"></bell-icon>
          <div class="tab-title">Ereignisse</div>
        </router-link>
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Systeminfo' }">
          <info-icon class="tab-icon"></info-icon>
          <div class="tab-title">Systeminfo</div>
        </router-link>
      </nav>
    </nav>
  </div>
</template>

<script>
import {ActivityIcon, SunIcon, SlidersIcon, DatabaseIcon, LogOutIcon, InfoIcon, BellIcon} from 'vue-feather-icons';
import featCompt from '../lib/feathercompt';

featCompt(ActivityIcon);
featCompt(SunIcon);
featCompt(SlidersIcon);
featCompt(DatabaseIcon);
featCompt(LogOutIcon);
featCompt(BellIcon);
featCompt(InfoIcon);

export default {
  name: 'SideBar',
  components: {
    ActivityIcon, SunIcon, SlidersIcon, DatabaseIcon, LogOutIcon, InfoIcon, BellIcon
  }
}
</script>

<style>

  .nav-link {
    -webkit-user-drag: none;
    padding: 10px 40px 10px 40px;
    margin-left: 50px;
    margin-right: 50px;
  }

  .nav {
    width: max-content;
    margin-left: auto;
    margin-right: auto;
  }

  .nav .nav {
    display: none;
  }

  .nav-box {
    padding-top: 5px;
    padding-bottom: 5px;
    height: auto !important;
    bottom: 0;
    position: absolute;
    width: 100%;
  }

  .tab-title {
    display: none;
  }

  .tab-icon {
    width: 35px;
    height: 35px;
  }

  @media (min-width: 992px) {
    .nav {
      width: auto;
    }

    .nav .nav {
      padding-left: 30px;
      margin: 0;
      display: block;
      position: relative;
    }

    .nav-link {
      -webkit-user-drag: auto;
      padding: .5rem 1rem;
      margin: 2px 0;
    }

    .nav-box {
      height: 100% !important;
      position: relative;
      display: block !important;
      width: auto;
    }

    .tab-title {
      display: inline;
      padding-left: 5px;
      vertical-align: middle;
    }

    .tab-icon {
      width: auto;
      height: auto;
    }
  }

</style>