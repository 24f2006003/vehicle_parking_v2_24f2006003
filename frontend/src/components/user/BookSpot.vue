<template>
  <div class="container">
    <div class="card shadow-sm mx-auto" style="max-width: 600px;">
      <div class="card-header bg-warning text-dark">
        <h4 class="mb-0">Book a Parking Spot</h4>
      </div>
      <div class="card-body">
        <p class="text-muted mb-4">Reserve a parking spot for your upcoming visit. Spot will be auto-assigned.</p>

        <form @submit.prevent="submitReservation">
          <div class="mb-3">
            <label class="form-label">Parking Lot</label>
            <select v-model="form.lotId" class="form-select" required>
              <option value="">-- Select Lot --</option>
              <option v-for="lot in lots" :key="lot.id" :value="lot.id">
                {{ lot.prime_location_name }} ({{ lot.price }}/hr)
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Vehicle Number</label>
            <input v-model="form.vehicleNumber" type="text" class="form-control" required
              placeholder="e.g. MH12AB1234" />
          </div>

          <div class="row mb-4">
            <div class="col-md-6">
              <label class="form-label">From</label>
              <input type="datetime-local" v-model="form.from" class="form-control" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">To</label>
              <input type="datetime-local" v-model="form.to" class="form-control" required />
            </div>
          </div>

          <div class="d-grid">
            <button type="submit" class="btn btn-primary" :disabled="loading || !form.lotId">
              Reserve Spot
            </button>
          </div>

          <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const lots = ref([])
const loading = ref(false)
const error = ref('')

const form = reactive({
  lotId: '',
  vehicleNumber: '',
  from: '',
  to: ''
})

onMounted(async () => {
  loading.value = true
  try {
    const { data } = await api.get('/api/lots')
    lots.value = data
  } catch (e) {
    error.value = 'Could not load lots'
  } finally {
    loading.value = false
  }
})

async function submitReservation() {
  if (!form.lotId) return
  loading.value = true
  error.value = ''

  try {
    // Calculate estimated cost
    const selectedLot = lots.value.find(l => l.id === form.lotId)
    const start = new Date(form.from)
    const end = new Date(form.to)
    const hours = (end - start) / 36e5
    const cost = selectedLot ? Math.max(0, (hours * selectedLot.price).toFixed(2)) : 0

    await api.post('/api/reservations', {
      lot_id: form.lotId,
      parking_timestamp: form.from, // Correct key expected by backend
      leaving_timestamp: form.to,   // Correct key expected by backend
      parking_cost: cost
    })
    alert('Reservation successful!')
    router.push('/user/history')
  } catch (e) {
    error.value = 'Reservation failed: ' + (e.response?.data?.message || e.message)
  } finally {
    loading.value = false
  }
}
</script>
