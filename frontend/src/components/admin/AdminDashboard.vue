<template>
  <div class="admin-dashboard">
    <section>
      <h1>Admin Dashboard</h1>
      <p>Quick links</p>
      <p v-if="loading">Loading...</p>
      <p v-if="error">{{ error }}</p>
      <ul v-if="!loading && !error">
        <li>Total users: {{ data.total_users }}</li>
        <li>Total reservations: {{ data.total_reservations }}</li>
        <li>Total parking lots: {{ data.total_parking_lots }}</li>
      </ul>
      <div class="links">
        <router-link to="/admin/add-lot">Add Parking Lot</router-link>
        <router-link to="/admin/view-lots">View Lots</router-link>
        <router-link to="/admin/users">Registered Users</router-link>
        <router-link to="/admin/occupied">Occupied Spots</router-link>
        <router-link to="/admin/summary">Summary</router-link>
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
  if (!token) { loading.value = false; return }
  try {
    const res = await fetch('/api/dashboard', { headers: { Authorization: `Bearer ${token}` } })
    if (!res.ok) throw new Error()
    const d = await res.json()
    data.value = { total_users: d.total_users, total_reservations: d.total_reservations, total_parking_lots: d.total_parking_lots }
  } catch (e) {
    error.value = 'Login as admin to view summary'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.admin-dashboard { display: flex; flex-direction: column; gap: 1rem; padding: 1rem; }
.links { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.content-area { min-height: 200px; padding: 0.5rem; border: 1px solid; }
</style>
