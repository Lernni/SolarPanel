<template>
  <div id="sidebar" class="bg-light h-100">
    <b-navbar-brand>
      SolarPanel
    </b-navbar-brand>
    <b-nav vertical pills>
      <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'dashboard' }">
        <!-- <sun-icon class="tab-icon"></sun-icon> -->
        <div class="tab-title">
          Dashboard
          <span class="badge badge-pill badge-secondary">pause</span>
        </div>
      </router-link>
      <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Messwerte' }">
        <!-- <activity-icon class="tab-icon"></activity-icon> -->
        <div class="tab-title">Messwerte</div>
      </router-link>
      <nav class="nav nav-pills flex-lg-column" role="tablist">
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Browser' }">
          <!-- <database-icon class="tab-icon"></database-icon> -->
          <div class="tab-title">Browser</div>
        </router-link>
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Export' }">
          <!-- <log-out-icon class="tab-icon"></log-out-icon> -->
          <div class="tab-title">Export</div>
        </router-link>
      </nav>
      <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'System' }">
        <!-- <sliders-icon class="tab-icon"></sliders-icon> -->
        <div class="tab-title">System</div>
      </router-link>
      <nav class="nav nav-pills flex-lg-column" role="tablist">
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'settings' }">
          <!-- <sliders-icon class="tab-icon"></sliders-icon> -->
          <div class="tab-title">Einstellungen</div>
        </router-link>
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Ereignisse' }">
          <!-- <bell-icon class="tab-icon"></bell-icon> -->
          <div class="tab-title">
            Ereignisse
            <span class="badge badge-pill badge-primary">8</span>
          </div>
        </router-link>
        <router-link class="nav-link" data-toggle="pill" role="tab" :to="{ name: 'Systeminfo' }">
          <!-- <info-icon class="tab-icon"></info-icon> -->
          <div class="tab-title">
            Systeminfo
            <span class="badge badge-pill badge-danger">!</span>
          </div>
        </router-link>
      </nav>
    </b-nav>
  </div>
</template>

<script>
export default {
  name: 'SideBar'
}
</script>

<style scoped>

  #sidebar .nav-link {
    -webkit-user-drag: none;
    padding: 10px 40px 10px 40px;
    margin-left: 50px;
    margin-right: 50px;
  }

  #sidebar .nav-link .tab-icon {
    width: 35px;
    height: 35px;
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
      padding-left: 20px;
      margin: 0;
      display: block;
      position: relative;
    }

    #sidebar .nav-link {
      -webkit-user-drag: auto;
      padding: .5rem 1rem;
      margin: 2px 0;
      font-size: inherit;
    }

    #sidebar .nav-link .tab-title {
      display: inline;
      padding-left: 5px;
      vertical-align: middle;
    }

    #sidebar .nav-link .tab-icon {
      width: auto;
      height: auto;
    }

    .nav-box {
      height: 100% !important;
      position: relative;
      display: block !important;
      width: auto;
    }
  }

</style>