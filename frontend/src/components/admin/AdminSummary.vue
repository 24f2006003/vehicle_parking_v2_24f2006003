<template>
  <div>
    <h4 class="mb-4 border-start border-4 border-success ps-2">Admin Summary</h4>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>

    <div v-else>
      <!-- Stats Cards -->
      <div class="row g-4 mb-5">
        <div class="col-md-4">
          <div class="card text-white bg-primary h-100">
            <div class="card-body">
              <h5 class="card-title">Total Users</h5>
              <p class="display-4">{{ data.total_users }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-success h-100">
            <div class="card-body">
              <h5 class="card-title">Total Lots</h5>
              <p class="display-4">{{ data.total_parking_lots }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-info h-100">
            <div class="card-body">
              <h5 class="card-title">Reservations</h5>
              <p class="display-4">{{ data.total_reservations }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Section (Simulated with Bootstrap) -->
      <div class="row g-4">
        <div class="col-md-12">
          <div class="card h-100">
            <div class="card-header fw-bold">Occupancy Overview</div>
            <div class="card-body">
              <div v-if="occupancyData.length === 0" class="text-muted">No parking lots available.</div>
              <div v-for="lot in occupancyData" :key="lot.name" class="mb-3">
                <div class="d-flex justify-content-between mb-1">
                  <span>{{ lot.name }}</span>
                  <span>{{ lot.percent }}% ({{ lot.occupied }}/{{ lot.total }})</span>
                </div>
                <div class="progress">
                  <div class="progress-bar" role="progressbar" :style="{ width: lot.percent + '%' }"
                    :aria-valuenow="lot.percent" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const data = ref({ total_users: 0, total_reservations: 0, total_parking_lots: 0 })
const occupancyData = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    // Fetch summary data
    const { data: d } = await api.get('/api/dashboard')
    data.value = d

    // Fetch lots for occupancy
    const { data: lots } = await api.get('/api/lots')
    occupancyData.value = lots.map(lot => {
      const occupied = lot.number_of_spots - lot.available_spots
      const percent = lot.number_of_spots > 0 ? Math.round((occupied / lot.number_of_spots) * 100) : 0
      return {
        name: lot.prime_location_name,
        occupied,
        total: lot.number_of_spots,
        percent
      }
    })
  } catch (e) {
    error.value = 'Could not load summary data'
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>
