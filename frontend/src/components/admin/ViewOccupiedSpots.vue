<template>
  <div>
    <h2>Occupied Spots</h2>
    <div>
      <label>
        Select Lot
        <select v-model.number="selectedLot" @change="loadSpots">
          <option disabled :value="0">Choose a lot</option>
          <option v-for="lot in lots" :key="lot.lot_id" :value="lot.lot_id">{{ lot.prime_location_name }}</option>
        </select>
      </label>
    </div>

    <p v-if="loading">Loading...</p>
    <p v-if="error">{{ error }}</p>

    <table v-if="!loading && !error && spots.length">
      <thead>
        <tr>
          <th>Spot</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in spots" :key="s.spot_id">
          <td>{{ s.spot_id }}</td>
          <td>{{ s.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const lots = ref([])
const spots = ref([])
const selectedLot = ref(0)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    const res = await fetch('/api/lots')
    if (!res.ok) throw new Error()
    lots.value = await res.json()
  } catch (e) {
    error.value = 'Could not load lots'
  }
})

async function loadSpots() {
  if (!selectedLot.value) return
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`/api/lots/${selectedLot.value}/spots?status=O`)
    if (!res.ok) throw new Error()
    spots.value = await res.json()
  } catch (e) {
    error.value = 'Could not load spots'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
th, td { border: 1px solid; padding: 0.5rem; text-align: left; }
</style>
