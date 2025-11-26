<template>
  <div class="admin-dashboard container-fluid p-0">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom px-4">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-success">Welcome to Admin</span>
        <div class="d-flex align-items-center">
          <ul class="nav nav-pills me-4">
            <li class="nav-item">
              <router-link to="/admin/view" class="nav-link" active-class="active">View</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/users" class="nav-link" active-class="active">Users</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/search" class="nav-link" active-class="active">Search</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/summary" class="nav-link" active-class="active">Summary</router-link>
            </li>
          </ul>
          <a href="#" class="text-danger text-decoration-none" @click.prevent="logout">Logout</a>
        </div>
      </div>
    </nav>

    <!-- Content Area -->
    <div class="p-4">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function logout() {
  localStorage.removeItem('token')
  router.push('/')
}
</script>

<style scoped>
.nav-link {
  color: #495057;
  font-weight: 500;
}
.nav-link.active {
  background-color: #198754 !important; /* Bootstrap success color */
  color: white !important;
}
</style>
