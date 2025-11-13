<template>
  <div class="admin-dashboard">
    <section>
      <h1>Admin Dashboard</h1>
      <p v-if="loading">Loading...</p>
      <p v-if="error">{{ error }}</p>
      <ul v-if="!loading && !error">
        <li>Total users: {{ data.total_users }}</li>
        <li>Total reservations: {{ data.total_reservations }}</li>
        <li>Total parking lots: {{ data.total_parking_lots }}</li>
      </ul>
      <div class="mb-2">
        <router-link class="btn btn-outline-primary btn-sm me-2" to="/admin/add-lot">Add Parking Lot</router-link>
        <router-link class="btn btn-outline-primary btn-sm me-2" to="/admin/view-lots">View Lots</router-link>
        <router-link class="btn btn-outline-primary btn-sm me-2" to="/admin/users">Registered Users</router-link>
        <router-link class="btn btn-outline-primary btn-sm me-2" to="/admin/occupied">Occupied Spots</router-link>
        <router-link class="btn btn-outline-primary btn-sm" to="/admin/summary">Summary</router-link>
      </div>
    </section>

    <section class="content-area">
      <router-view />
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const data = ref({ total_users: 0, total_reservations: 0, total_parking_lots: 0 })
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { loading.value = false; error.value = 'Please login'; return }
  try {
    const adminCheck = await fetch('/api/admin_home', { headers: { Authorization: `Bearer ${token}` } })
    if (!adminCheck.ok) { error.value = 'Login as admin to view summary'; return }
    const res = await fetch('/api/dashboard', { headers: { Authorization: `Bearer ${token}` } })
    if (!res.ok) { error.value = 'Could not load dashboard'; return }
    const d = await res.json()
    data.value = { total_users: d.total_users, total_reservations: d.total_reservations, total_parking_lots: d.total_parking_lots }
  } catch (e) {
    error.value = 'Could not load dashboard'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.admin-dashboard { display: flex; flex-direction: column; gap: 1rem; padding: 1rem; }
.content-area { min-height: 200px; padding: 0.5rem; border: 1px solid; }
</style>
