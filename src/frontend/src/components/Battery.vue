<template>
  <div class="progress" ref="progress">
    <div class="progress-value"><span>{{soc}}</span>%</div>
    <div v-bind:style="{ height: soc * 0.98 + '%' }" class="progress-bar" role="progressbar" v-bind:aria-valuenow=soc aria-valuemin="0" aria-valuemax="100"></div>
  </div>
</template>

<script>
export default {
  name: 'Battery',
  props: {
    soc: Number
  }
}
</script>

<style lang="scss">

  .progress::after {
    content: " ";
    position: absolute;
    z-index: 1;
    top: -1px;
    right: 0;
    bottom: 0;
    left: 0;
    border: 5px solid white;
    border-top: 6px solid white;
    border-radius: 10px;
    text-align: center;
    line-height: 250px;
  }

	.progress {
    position: relative;
    height: 250px !important;
    width: 100px;
    border-radius: 10px !important;
    border: 5px solid #e9ecef;
	}

  .progress-value {
    z-index: 2;
    text-align: center;
    vertical-align: middle;
    width: 100%;
    line-height: 240px;
    font-size: 20px;
  }

  .progress-value span {
    font-size: 30px;
    font-weight: 600;
  }

	.progress-bar {
    position: absolute;
    width: 94%;
    margin-left: auto;
    margin-right: auto;
    left: 0;
    right: 0;
    bottom: 0;
    margin-bottom: 3px;
    transition: height .6s ease !important;
    background: #00ebb9;
    background: linear-gradient(30deg, rgba(0,235,170,1) 0%, rgba(0,235,138,1) 100%);
    border-radius: 10px;
	}

</style>