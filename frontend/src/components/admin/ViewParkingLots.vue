<template>
  <div>
    <h2>Parking Lots</h2>
    <div>
      <label>
        Search
        <input v-model="filters.name" />
      </label>
      <label>
        Min available
        <input v-model.number="filters.minAvailable" type="number" min="0" />
      </label>
    </div>

    <p v-if="loading">Loading...</p>
    <p v-if="error">{{ error }}</p>

    <table v-if="!loading && !error">
      <thead>
        <tr>
          <th>#</th>
          <th>Location</th>
          <th>Address</th>
          <th>Pin</th>
          <th>Rate</th>
          <th>Spots</th>
          <th>Available</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="lot in filteredLots" :key="lot.lot_id">
          <td>{{ lot.lot_id }}</td>
          <td>{{ lot.prime_location_name }}</td>
          <td>{{ lot.address }}</td>
          <td>{{ lot.pin_code }}</td>
          <td>{{ lot.price }}</td>
          <td>{{ lot.number_of_spots }}</td>
          <td>{{ lot.available_spots }}</td>
          <td>
            <router-link :to="`/admin/edit-lot/${lot.lot_id}`">Edit</router-link>
            <router-link :to="`/admin/add-spots/${lot.lot_id}`">Add Spots</router-link>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'

const lots = ref([])
const loading = ref(true)
const error = ref('')

const filters = reactive({ name: '', minAvailable: 0 })

onMounted(async () => {
  try {
    const res = await fetch('/api/lots')
    if (!res.ok) throw new Error('Failed')
    lots.value = await res.json()
  } catch (e) {
    error.value = 'Could not load lots'
  } finally {
    loading.value = false
  }
})

const filteredLots = computed(() => {
  const name = (filters.name || '').toLowerCase()
  const minAvail = filters.minAvailable || 0
  return lots.value.filter((lot) =>
    lot.prime_location_name.toLowerCase().includes(name) &&
    (lot.available_spots >= minAvail)
  )
})
</script>

<style scoped>
table { width: 100%; border-collapse: collapse; }
th, td { border: 1px solid; padding: 0.5rem; text-align: left; }
div { padding: 0.5rem 0; }
</style>
