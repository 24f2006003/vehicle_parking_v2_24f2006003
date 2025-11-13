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

const current = ref(null)

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return
  try {
    const res = await fetch('/api/reservations', { headers: { Authorization: `Bearer ${token}` } })
    if (!res.ok) return
    const items = await res.json()
    current.value = Array.isArray(items) ? items.find(r => r.status === 'active') || items[0] : null
  } catch {}
})
</script>

<style scoped>
.user-dashboard { display: flex; flex-direction: column; gap: 1rem; padding: 1rem; }
.panel { padding: 1rem; border: 1px solid; }
nav { display: flex; gap: 0.5rem; }
.content { min-height: 200px; }
</style>
