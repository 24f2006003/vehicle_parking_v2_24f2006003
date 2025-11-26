<template>
  <div>
    <h4 class="mb-4 border-start border-4 border-success ps-2">Parking Lots</h4>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>

    <div v-else class="row g-4">
      <div class="col-md-6 col-lg-4" v-for="lot in lots" :key="lot.lot_id">
        <div class="card h-100 shadow-sm">
          <div class="card-header bg-light d-flex justify-content-between align-items-center">
            <span class="fw-bold">{{ lot.prime_location_name }}</span>
            <span class="badge bg-primary rounded-pill">{{ lot.number_of_spots }} Spots</span>
          </div>
          <div class="card-body">
            <div class="mb-3 small text-muted">
              <div>{{ lot.address }}</div>
              <div>Pin: {{ lot.pin_code }} | Rate: ${{ lot.price }}/hr</div>
            </div>

            <!-- Mini Spot Grid -->
            <div class="mb-3">
              <div class="d-flex justify-content-between small mb-1">
                <span>Status:</span>
                <span class="text-success">{{ lot.available_spots }} Available</span>
              </div>
              <div class="spots-grid">
                <span
                  v-for="n in Math.min(lot.number_of_spots, 20)"
                  :key="n"
                  class="spot-dot"
                  :class="getSpotClass(lot, n)"
                  :title="n <= (lot.number_of_spots - lot.available_spots) ? 'Occupied' : 'Available'"
                ></span>
                <span v-if="lot.number_of_spots > 20" class="small text-muted ms-1">...</span>
              </div>
            </div>

            <div class="d-flex gap-2 mt-auto">
              <router-link :to="`/admin/edit-lot/${lot.lot_id}`" class="btn btn-sm btn-outline-warning flex-grow-1">Edit</router-link>
              <router-link :to="`/admin/add-spots/${lot.lot_id}`" class="btn btn-sm btn-outline-secondary flex-grow-1">Spots</router-link>
              <button class="btn btn-sm btn-outline-danger" @click="deleteLot(lot)">Delete</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Lot Card -->
      <div class="col-md-6 col-lg-4">
        <div class="card h-100 border-dashed d-flex align-items-center justify-content-center bg-light" style="min-height: 200px; cursor: pointer;" @click="$router.push('/admin/add-lot')">
          <div class="text-center text-muted">
            <div class="fs-1">+</div>
            <div>Add Parking Lot</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const lots = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get('/api/lots')
    lots.value = data
  } catch (e) {
    error.value = 'Could not load lots'
  } finally {
    loading.value = false
  }
})

function getSpotClass(lot, index) {
  // Naive visualization: First (Total - Available) are occupied
  const occupiedCount = lot.number_of_spots - lot.available_spots
  return index <= occupiedCount ? 'bg-danger' : 'bg-success'
}

async function deleteLot(lot) {
  if (!confirm(`Delete ${lot.prime_location_name}?`)) return
  try {
    await api.delete(`/api/lots/${lot.lot_id}`)
    lots.value = lots.value.filter(l => l.lot_id !== lot.lot_id)
  } catch (e) {
    alert('Failed to delete lot')
  }
}
</script>

<style scoped>
.border-dashed {
  border: 2px dashed #dee2e6;
  transition: all 0.2s;
}
.border-dashed:hover {
  border-color: #0d6efd;
  background-color: #e9ecef !important;
}
.spots-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.spot-dot {
  width: 12px;
  height: 12px;
  border-radius: 2px;
  display: inline-block;
}
</style>
