<script setup></script>

<template>
  <div>
    <header v-if="$route.meta.title" class="bg-white shadow">
      <div class="py-6 px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold leading-tight text-gray-900">
          {{ $route.meta.title }}
        </h1>
      </div>
    </header>
    <main class="flex justify-center">
      <router-view />
    </main>
  </div>
</template>
