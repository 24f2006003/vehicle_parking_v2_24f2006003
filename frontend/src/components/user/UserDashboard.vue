<template>
  <div class="user-dashboard">
    <header class="panel">
      <h1>User Dashboard</h1>
      <p>Manage your parking reservations and track history.</p>
    </header>

    <section class="quick-info panel">
      <h2>Current Reservation</h2>
      <div v-if="current">
        <p><strong>Spot:</strong> {{ current.spot_id }}</p>
        <p><strong>Status:</strong> {{ current.status }}</p>
      </div>
      <p v-else>No active reservations right now.</p>
    </section>

    <nav class="panel">
      <router-link to="/user/book/1">Book Spot</router-link>
      <router-link to="/user/release/101">Release Spot</router-link>
      <router-link to="/user/history">History</router-link>
      <router-link to="/user/summary">Summary</router-link>
    </nav>

    <section class="content panel">
      <h2>Selected Module</h2>
      <router-view />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const current = ref(null)
const reservations = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { loading.value = false; error.value = 'Please login'; return }
  try {
    const { data } = await api.get('/api/reservations')
    reservations.value = data
    current.value = Array.isArray(data) ? data.find(r => r.status === 'active') || data[0] : null
  } catch (e) {
    error.value = 'Could not load reservations'
  } finally {
    loading.value = false
  }
})
</script>
