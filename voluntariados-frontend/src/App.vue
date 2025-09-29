<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
// import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <img alt="Vue logo" src="./assets/logo.svg" width="125" height="125" />
    <div class="wrapper">
      <!-- <HelloWorld msg="¡Bienvenido a tu aplicación Vue 3!" /> -->
      <nav>
        <RouterLink to="/">Inicio</RouterLink>
        <RouterLink to="/about">Acerca de</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

/* Más estilos... */
</style>