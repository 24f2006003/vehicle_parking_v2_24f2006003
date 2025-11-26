<template>
  <div class="container">
    <h3 class="mb-4 border-start border-4 border-primary ps-2">User Summary</h3>

    <div class="row g-4">
      <div class="col-md-4">
        <div class="card text-white bg-primary h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Total Reservations</h5>
            <p class="display-4 fw-bold mb-0">{{ summary.totalReservations }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-info h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Hours Parked</h5>
            <p class="display-4 fw-bold mb-0">{{ summary.hoursParked }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-success h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Amount Spent (₹)</h5>
            <p class="display-4 fw-bold mb-0">{{ summary.amountSpent }}</p>
          </div>
        </div>
      </div>
    </div>
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
    summary.value.hoursParked = data.length * 1 // Mock calculation
  } catch {}
})
</script>
