<template>
  <div class="nav-box bg-light h-100">
    <div class="nav flex-lg-column nav-pills bg-light" id="v-pills-tab" role="tablist" aria-orientation="vertical">
      <router-link v-for="(r,i) in routes" :key="i" :route="r" :to=r.path class="nav-link" data-toggle="pill" role="tab" aria-selected="true">
        <sun-icon v-if="r.icon === 'dashboard'" class="tab-icon"></sun-icon>
        <activity-icon v-if="r.icon === 'stats'" class="tab-icon"></activity-icon>
        <sliders-icon v-if="r.icon === 'settings'" class="tab-icon"></sliders-icon>
        <div class="tab-title">{{r.name}}</div>
      </router-link>
    </div>
  </div>
</template>

<script>
import {ActivityIcon, SunIcon, SlidersIcon} from 'vue-feather-icons';
import featCompt from '../lib/feathercompt';

featCompt(ActivityIcon);
featCompt(SunIcon);
featCompt(SlidersIcon);

export default {
  name: 'SideBar',
  components: {
    ActivityIcon, SunIcon, SlidersIcon
  },
  computed: {
    routes() {
      return this.$router.options.routes
    }
  }
}
</script>

<style scoped>

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
      height: 100%;
      width: 100%;
    }

    .nav-link {
      -webkit-user-drag: auto;
      padding: .5rem 1rem;
      margin: 0;
    }

    .nav-box {
      height: 100% !important;
      position: relative;
      width: auto;
    }

    .tab-title {
      display: inline;
      padding-left: 5px;
    }

    .tab-icon {
      width: auto;
      height: auto;
    }
  }

</style>