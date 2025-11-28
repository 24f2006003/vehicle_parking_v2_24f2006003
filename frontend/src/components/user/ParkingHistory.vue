<template>
  <div class="container">
    <h3 class="mb-4 border-start border-4 border-primary ps-2">Parking History</h3>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="!loading && !error" class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-striped table-hover mb-0">
            <thead class="table-light">
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
                <td>{{ item.lot_name || item.lot_id || '-' }}</td>
                <td>{{ item.spot_id }}</td>
                <td>{{ new Date(item.parking_timestamp).toLocaleString() }}</td>
                <td>{{ item.leaving_timestamp ? new Date(item.leaving_timestamp).toLocaleString() : '-' }}</td>
                <td>
                  <span class="badge" :class="getStatusClass(item.status)">{{ item.status }}</span>
                </td>
                <td>{{ item.parking_cost ? item.parking_cost.toFixed(2) : '0.00' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
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

function getStatusClass(status) {
  switch (status) {
    case 'active': return 'bg-success';
    case 'completed': return 'bg-secondary';
    case 'cancelled': return 'bg-danger';
    default: return 'bg-info';
  }
}
</script>
