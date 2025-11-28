<template>
  <div class="container py-4">
    <h3 class="mb-4 border-start border-4 border-danger ps-2">Occupied Spots</h3>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <label class="form-label fw-bold">Select Lot:</label>
        <select v-model="selectedLot" class="form-select w-auto d-inline-block ms-2">
          <option value="">-- All Lots --</option>
          <option v-for="lot in lots" :key="lot.id" :value="lot.id">
            {{ lot.prime_location_name }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="spots.length" class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-striped table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>Lot Name</th>
                <th>Spot Number</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="spot in spots" :key="spot.spot_id">
                <td>{{ spot.lot_name || '-' }}</td>
                <td>{{ spot.spot_id }}</td>
                <td>
                  <span class="badge bg-danger">Occupied</span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-danger" @click="forceRelease(spot)">Force Release</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else-if="!loading" class="alert alert-info">
      No occupied spots found.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../../api'

const lots = ref([])
const selectedLot = ref('')
const spots = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get('/api/lots')
    lots.value = data
    await fetchSpots()
  } catch (e) {
    error.value = 'Could not load data'
    console.error(e)
  } finally {
    loading.value = false
  }
})

watch(selectedLot, async () => {
  await fetchSpots()
})

async function fetchSpots() {
  loading.value = true
  try {
    let url = '/api/spots/occupied'
    if (selectedLot.value) {
      url = `/api/lots/${selectedLot.value}/spots`
    }
    const { data } = await api.get(url, { params: { status: 'O' } })
    spots.value = data
  } catch (e) {
    error.value = 'Could not load spots'
  } finally {
    loading.value = false
  }
}

async function forceRelease(spot) {
  if (!confirm(`Force release spot ${spot.spot_id}?`)) return

  try {
    if (spot.reservation_id) {
      // If there's a reservation, complete it
      await api.patch(`/api/reservations/${spot.reservation_id}`, { action: 'complete' })
    } else {
      // If no reservation (phantom occupancy), just free the spot
      await api.patch(`/api/spots/${spot.spot_id}`, { status: 'A' })
    }
    // Refresh list
    await fetchSpots()
    alert('Spot released successfully')
  } catch (e) {
    alert('Failed to release spot: ' + (e.response?.data?.message || e.message))
  }
}

</script>
