<template>
  <div id="sidebar" class="bg-light h-100">
    <b-nav vertical pills>
      <b-nav-item :to="{ name: 'dashboard' }" exact exact-active-class="active">
        <b-icon icon="brightness-high-fill"></b-icon>
        Dashboard
      </b-nav-item>
      <b-nav-item :to="{ name: 'browser' }" exact exact-active-class="active">
        <b-icon icon="bar-chart-fill"></b-icon>
        Messwerte
      </b-nav-item>
      <b-nav-item :to="{ name: 'settings' }" exact exact-active-class="active">
        <b-icon icon="sliders"></b-icon>
        Einstellungen
      </b-nav-item>
    </b-nav>
  </div>
</template>

<script>
export default {
  name: 'SideBar'
}
</script>

<style scoped>

  /* #sidebar .nav-link {
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
  } */

  @media (min-width: 992px) {
    /* .nav {
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
    } */
  }

</style>