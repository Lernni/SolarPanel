<script setup>
import Nav from './components/Nav.vue'
</script>

<template>
  <div>
    <main class="m-3 flex flex-wrap">
      <div
        :class="
          'z-50 bg-white fixed inset-x-0 bottom-0 order-1 mx-auto flex grow justify-center text-center ' +
          'sm:bg-transparent sm:relative sm:-order-1 sm:text-left md:block md:grow-0 md:flex-wrap'
        "
      >
        <Nav />
      </div>
      <div class="mb-10 grow">
        <div class="flex justify-center">
          <router-view />
        </div>
      </div>
    </main>
  </div>
</template>
