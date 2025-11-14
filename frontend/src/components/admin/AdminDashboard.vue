<template>
  <div class="admin-dashboard container-fluid py-2">
    <div class="bg-success bg-opacity-25 rounded px-3 py-2 d-flex align-items-center justify-content-between">
      <div class="fw-semibold">Welcome to Admin</div>
      <a href="#" class="text-decoration-underline" @click.prevent>Edit Profile</a>
    </div>

    <ul class="nav nav-pills my-3">
      <li class="nav-item"><a class="nav-link active" href="#" @click.prevent>Home</a></li>
      <li class="nav-item"><router-link class="nav-link" to="/admin/users">Users</router-link></li>
      <li class="nav-item"><a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Search</a></li>
      <li class="nav-item"><router-link class="nav-link" to="/admin/summary">Summary</router-link></li>
      <li class="nav-item"><a class="nav-link" href="#" @click.prevent="logout">Logout</a></li>
    </ul>

    <h5 class="border rounded px-3 py-2 mb-3">Parking Lots</h5>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>

    <div v-else class="row g-3">
      <div class="col-sm-6 col-md-4 col-lg-3" v-for="lot in lots" :key="lot.lot_id">
        <div class="card h-100">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-start mb-1">
              <h6 class="card-title mb-0">{{ lot.prime_location_name }}</h6>
              <div class="small">
                <a href="#" class="me-2" @click.prevent="editLot(lot)">Edit</a>
                <a href="#" class="text-danger" @click.prevent="deleteLot(lot)">Delete</a>
              </div>
            </div>
            <div class="text-success small mb-2">Occupied : {{ lot.number_of_spots - lot.available_spots }}/{{ lot.number_of_spots }}</div>

            <div class="spots-grid">
              <span
                v-for="n in Math.min(lot.number_of_spots, 16)"
                :key="n"
                class="spot"
                :class="spotClass(lot, n)"
                title="Spot"
              ></span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center my-4">
      <router-link to="/admin/add-lot" class="btn btn-primary">+ Add Lot</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const loading = ref(true)
const error = ref('')
const lots = ref([])
const router = useRouter()

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { loading.value = false; error.value = 'Please login'; return }
  try {
    await api.get('/api/admin_home')
    const { data } = await api.get('/api/lots')
    lots.value = data
  } catch (e) {
    error.value = 'Could not load lots'
  } finally {
    loading.value = false
  }
})

function logout() {
  localStorage.removeItem('token')
  router.push('/')
}

function spotClass(lot, index) {
  // naive distribution: first N-available spots are occupied markers
  const occupiedCount = lot.number_of_spots - lot.available_spots
  return index <= occupiedCount ? 'occupied' : 'available'
}

function editLot(lot) {
  router.push(`/admin/edit-lot/${lot.lot_id}`)
}

async function deleteLot(lot) {
  const token = localStorage.getItem('token')
  if (!token) return
  if (!confirm('Delete this lot?')) return
  try {
    await api.delete(`/api/lots/${lot.lot_id}`)
    lots.value = lots.value.filter(l => l.lot_id !== lot.lot_id)
  } catch (e) {
    // no-op
  }
}
</script>

<style scoped>
.spots-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }
.spot { display: inline-block; width: 20px; height: 20px; border-radius: 4px; border: 1px solid #999; }
.spot.available { background: #a7e3a7; }
.spot.occupied { background: #f4a7a7; }
</style>
