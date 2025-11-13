<script setup>
// import LoginPage from './components/LoginPage.vue'
import NavPage from './components/NavPage.vue'
import FootPage from './components/FootPage.vue'
// import AdminPage from './components/AdminPage.vue'
import { RouterView } from 'vue-router';
</script>

<template>
  <NavPage />
  <!-- <LoginPage/> -->
  <!-- <AdminPage/> -->
  <RouterView />
  <FootPage />
</template>

<style scoped>

</style>
