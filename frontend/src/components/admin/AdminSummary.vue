<template>
  <div>
    <h2>Admin Summary</h2>
    <p v-if="loading">Loading...</p>
    <p v-if="error">{{ error }}</p>
    <ul v-if="!loading && !error">
      <li>Total users: {{ data.total_users }}</li>
      <li>Total reservations: {{ data.total_reservations }}</li>
      <li>Total parking lots: {{ data.total_parking_lots }}</li>
    </ul>
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
    if (!res.ok) { error.value = 'Could not load summary'; return }
    const d = await res.json()
    data.value = { total_users: d.total_users, total_reservations: d.total_reservations, total_parking_lots: d.total_parking_lots }
  } catch (e) {
    error.value = 'Could not load summary'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
ul { padding-left: 1rem; }
</style>
