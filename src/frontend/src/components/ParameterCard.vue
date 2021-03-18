<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">{{parameter}}</h5>
      <slot></slot>
      <h2 class="text-right">{{value}} {{unit}}</h2>
      <Sparkline height="100" :series="series"/>
    </div>
  </div>
</template> 

<script>
import Sparkline from './charts/Sparkline.vue'

export default {
  name: 'ParameterCard',
  components: {
    Sparkline
  },
  props: {
    parameter: String,
    value: Number,
    unit: String,
    color: String
  },
  data: (instance) => ({
    series: [{
      name: instance.parameter,
      data: [31, 40, 28, 51, 42, 109, 100],
      color: instance.color,
    }]
  })
}
</script>

<style lang="scss">

  .sparkline {
    margin: 0 -20px -20px -20px;
  }

  .card {
    width: 100%;
    flex: none !important;
    margin: 5px;
    
    h5, h2 {
      display: inline;
    }

    h2 {
      float: right;
    }
  }

  @media (min-width: 992px) {
    .card {
      flex: 1 0 0% !important;
      margin: 0;

      h5, h2 {
        display: block;
      }

      h2 {
        float: none;
      }
    }
  }
</style>