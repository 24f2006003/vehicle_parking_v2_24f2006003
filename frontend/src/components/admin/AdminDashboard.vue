<template>
  <div class="admin-dashboard min-vh-100 bg-light">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm px-4">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-uppercase tracking-wide">
          <i class="bi bi-shield-lock-fill me-2"></i>Admin<span class="text-success">Portal</span>
        </span>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#adminNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-end" id="adminNav">
          <ul class="navbar-nav align-items-center">
            <li class="nav-item">
              <router-link to="/admin/view" class="nav-link px-3" active-class="active">Lots</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/users" class="nav-link px-3" active-class="active">Users</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/reservations" class="nav-link px-3"
                active-class="active">Reservations</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/occupied" class="nav-link px-3" active-class="active">Occupancy</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/summary" class="nav-link px-3" active-class="active">Summary</router-link>
            </li>
            <li class="nav-item ms-lg-3">
              <button class="btn btn-outline-danger btn-sm rounded-pill px-4" @click.prevent="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Content Area -->
    <div class="container py-5">
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
.tracking-wide {
  letter-spacing: 1px;
}

.nav-link {
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #fff !important;
}

.nav-link.active {
  color: #198754 !important;
  /* Success green for admin */
  font-weight: 600;
}
</style>
