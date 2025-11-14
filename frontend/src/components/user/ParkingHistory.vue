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
import api from '../../api'

const history = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { loading.value = false; error.value = 'Please login'; return }
  try {
    const { data } = await api.get('/api/reservations')
    history.value = data
  } catch (e) {
    error.value = 'Could not load history'
  } finally {
    loading.value = false
  }
})
</script>
