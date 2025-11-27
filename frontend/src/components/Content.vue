<template>
  <NavPage />
  <main class="container py-5">
    <div class="px-4 py-5 my-5 text-center">
      <h1 class="display-5 fw-bold text-primary">Vehicle Parking System</h1>
      <div class="col-lg-6 mx-auto">
        <p class="lead mb-4">Secure, convenient, and smart parking management at your fingertips.</p>
        <div class="d-grid gap-2 d-sm-flex justify-content-sm-center">
          <router-link to="/login" class="btn btn-primary btn-lg px-4 gap-3">Login</router-link>
          <router-link to="/register" class="btn btn-outline-secondary btn-lg px-4">Register</router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import NavPage from './NavPage.vue';
</script>

<style scoped></style>