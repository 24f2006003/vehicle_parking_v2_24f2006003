<template>
  <div class="container-fluid py-4">
    <h3 class="mb-4">Search Parking Lots</h3>

    <div class="row mb-4">
      <div class="col-md-6">
        <div class="input-group">
          <input type="text" class="form-control" placeholder="Search by location or name..." v-model="searchQuery"
            @keyup.enter="performSearch">
          <button class="btn btn-primary" @click="performSearch">Search</button>
        </div>
      </div>
    </div>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>

    <div v-else-if="hasSearched && results.length === 0" class="alert alert-info">
      No parking lots found matching "{{ searchQuery }}".
    </div>

    <div v-else class="row g-3">
      <div class="col-sm-6 col-md-4 col-lg-3" v-for="lot in results" :key="lot.lot_id">
        <div class="card h-100">
          <div class="card-header bg-light fw-bold text-center">
            {{ lot.prime_location_name }}
          </div>
          <div class="card-body">
            <p class="card-text small mb-1"><strong>Address:</strong> {{ lot.address }}</p>
            <p class="card-text small mb-1"><strong>Pin:</strong> {{ lot.pin_code }}</p>
            <p class="card-text small mb-1"><strong>Rate:</strong> ₹{{ lot.price }}/hr</p>
            <p class="card-text small mb-3"><strong>Spots:</strong> {{ lot.number_of_spots }}</p>

            <div class="d-grid gap-2">
              <router-link :to="`/admin/edit-lot/${lot.lot_id}`" class="btn btn-sm btn-warning">Edit</router-link>
              <button class="btn btn-sm btn-danger" @click="deleteLot(lot)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../../api'

const searchQuery = ref('')
const results = ref([])
const loading = ref(false)
const error = ref('')
const hasSearched = ref(false)

async function performSearch() {
  if (!searchQuery.value.trim()) return
  loading.value = true
  error.value = ''
  hasSearched.value = true
  results.value = []

  try {
    // Fetch all lots and filter client-side for now as per typical small app patterns, 
    // or use a search endpoint if available. Assuming client-side filter for simplicity based on existing API.
    const { data } = await api.get('/api/lots')
    const query = searchQuery.value.toLowerCase()
    results.value = data.filter(lot =>
      lot.prime_location_name.toLowerCase().includes(query) ||
      lot.address.toLowerCase().includes(query) ||
      lot.pin_code.toString().includes(query)
    )
  } catch (e) {
    error.value = 'Search failed'
  } finally {
    loading.value = false
  }
}

async function deleteLot(lot) {
  if (!confirm('Delete this lot?')) return
  try {
    await api.delete(`/api/lots/${lot.lot_id}`)
    results.value = results.value.filter(l => l.lot_id !== lot.lot_id)
  } catch (e) {
    alert('Failed to delete lot: ' + (e.response?.data?.message || e.message))
  }
}
</script>
