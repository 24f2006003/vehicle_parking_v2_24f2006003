<template>
  <div class="user-summary">
    <h3>Summary</h3>
    <p>Snapshot of your parking usage.</p>

    <section class="cards">
      <article class="card">
        <h4>Total Reservations</h4>
        <p>{{ summary.totalReservations }}</p>
      </article>
      <article class="card">
        <h4>Hours Parked</h4>
        <p>{{ summary.hoursParked }}</p>
      </article>
      <article class="card">
        <h4>Amount Spent (₹)</h4>
        <p>{{ summary.amountSpent }}</p>
      </article>
    </section>

    <!-- Keep it simple: no chart/weekly breakdown -->
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const summary = ref({ totalReservations: 0, hoursParked: 0, amountSpent: 0 })

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return
  try {
    const res = await fetch('/api/reservations', { headers: { Authorization: `Bearer ${token}` } })
    if (!res.ok) return
    const items = await res.json()
    summary.value.totalReservations = items.length
    summary.value.amountSpent = items.reduce((s, r) => s + (r.parking_cost || 0), 0)
    summary.value.hoursParked = items.length * 1
  } catch {}
})
</script>

<style scoped>
.user-summary { display: flex; flex-direction: column; gap: 1rem; }
.cards { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.card { flex: 1; min-width: 160px; border: 1px solid; padding: 0.5rem; text-align: center; }
</style>
