<template>
  <b-navbar id="navbar" variant="light">
    <b-navbar-brand>
      {{ title }}
    </b-navbar-brand>
  </b-navbar>
</template>

<script>
export default {
  name: 'NavBar',
  props: {
    title: String
  }
}
</script>