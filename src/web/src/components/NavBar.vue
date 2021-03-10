<template>
  <nav class="navbar navbar-light bg-light d-none d-lg-flex">
    <span class="navbar-brand mb-0 h1">{{title}}</span>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    title: String
  }
}
</script>

<style>

</style>