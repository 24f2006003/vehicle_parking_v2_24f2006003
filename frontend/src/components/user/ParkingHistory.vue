<template>
  <div class="parking-history">
    <h3>Parking History</h3>
    <p>Past reservations with status and billing.</p>

    <p v-if="loading">Loading...</p>
    <p v-if="error">{{ error }}</p>

    <table v-if="!loading && !error">
      <thead>
        <tr>
          <th>#</th>
          <th>Lot</th>
          <th>Spot</th>
          <th>From</th>
          <th>To</th>
          <th>Status</th>
          <th>Amount (₹)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in history" :key="item.reservation_id">
          <td>{{ item.reservation_id }}</td>
          <td>{{ item.lot_id || '-' }}</td>
          <td>{{ item.spot_id }}</td>
          <td>{{ item.parking_timestamp }}</td>
          <td>{{ item.leaving_timestamp }}</td>
          <td>{{ item.status }}</td>
          <td>{{ item.parking_cost }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const history = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { loading.value = false; return }
  try {
    const res = await fetch('/api/reservations', { headers: { Authorization: `Bearer ${token}` } })
    if (!res.ok) throw new Error()
    history.value = await res.json()
  } catch (e) {
    error.value = 'Could not load history'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.parking-history { display: flex; flex-direction: column; gap: 1rem; }
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid; padding: 0.5rem; text-align: left; }
</style>
