<template>
  <div class="user-dashboard min-vh-100 bg-light">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm px-4">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-uppercase tracking-wide">
          <i class="bi bi-car-front-fill me-2"></i>Parking<span class="text-primary">App</span>
        </span>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav align-items-center">
            <li class="nav-item">
              <router-link to="/user/history" class="nav-link px-3" active-class="active">History</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/book/0" class="nav-link px-3" active-class="active">Book Spot</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/manage-bookings" class="nav-link px-3" active-class="active">Manage
                Bookings</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/summary" class="nav-link px-3" active-class="active">Summary</router-link>
            </li>
            <li class="nav-item ms-lg-3">
              <button class="btn btn-outline-danger btn-sm rounded-pill px-4" @click.prevent="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Content Area -->
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const current = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { loading.value = false; error.value = 'Please login'; return }
  try {
    // Attempt to fetch reservations to find active one
    const { data } = await api.get('/api/reservations')
    if (Array.isArray(data)) {
      current.value = data.find(r => r.status === 'active')
    }
  } catch (e) {
    console.error('Could not load active reservation')
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
  color: #0d6efd !important;
  font-weight: 600;
}
</style>
