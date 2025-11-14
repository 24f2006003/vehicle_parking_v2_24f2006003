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
import api from '../../api'

const summary = ref({ totalReservations: 0, hoursParked: 0, amountSpent: 0 })

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return
  try {
    const { data } = await api.get('/api/reservations')
    summary.value.totalReservations = data.length
    summary.value.amountSpent = data.reduce((s, r) => s + (r.parking_cost || 0), 0)
    summary.value.hoursParked = data.length * 1
  } catch {}
})
</script>
