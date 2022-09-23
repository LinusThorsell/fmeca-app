<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
    <div id="app">
    <header>
      <Navbar />
    </header>
  </div>
  <RouterView />
</template>

<style scoped>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  body {
    font-family: 'montserrat', sans-serif;
  }
  header {
    width: 100vw;
    background-color: #222;
    padding: 15px;
  }
</style>

<script>
  import Navbar from './components/Navbar.vue';
  export default {
    name: 'app',
    components: {
      Navbar
    }
  }
  </script>
  
