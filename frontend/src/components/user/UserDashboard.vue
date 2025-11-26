<template>
  <div class="user-dashboard container-fluid p-0">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom px-4">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-primary">Welcome User</span>
        <div class="d-flex align-items-center">
          <ul class="nav nav-pills me-4">
            <li class="nav-item">
              <router-link to="/user/history" class="nav-link" active-class="active">History</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/book/0" class="nav-link" active-class="active">Book Spot</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/release/0" class="nav-link" active-class="active">Release Spot</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/summary" class="nav-link" active-class="active">Summary</router-link>
            </li>
          </ul>
          <a href="#" class="text-danger text-decoration-none" @click.prevent="logout">Logout</a>
        </div>
      </div>
    </nav>

    <!-- Content Area -->
    <div class="container py-4">
      <!-- Quick Info Card -->
      <div class="card shadow-sm mb-4 border-start border-4 border-primary">
        <div class="card-body">
          <h5 class="card-title">Current Reservation</h5>
          <div v-if="current">
            <p class="mb-1"><strong>Spot:</strong> {{ current.spot_id }}</p>
            <p class="mb-0"><strong>Status:</strong> <span class="badge bg-success">{{ current.status }}</span></p>
          </div>
          <p v-else class="text-muted mb-0">No active reservations right now.</p>
        </div>
      </div>

      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const current = ref(null)
const reservations = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { loading.value = false; error.value = 'Please login'; return }
  try {
    // Attempt to fetch reservations if endpoint exists
    // const { data } = await api.get('/api/reservations')
    // reservations.value = data
    // current.value = Array.isArray(data) ? data.find(r => r.status === 'active') || data[0] : null
  } catch (e) {
    error.value = 'Could not load reservations'
  } finally {
    loading.value = false
  }
})

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
  background-color: #0d6efd !important;
  color: white !important;
}
</style>
