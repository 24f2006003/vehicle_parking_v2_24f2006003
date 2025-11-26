<template>
  <div class="container">
    <div class="card shadow-sm mx-auto" style="max-width: 600px;">
      <div class="card-header bg-warning text-dark">
        <h4 class="mb-0">Book a Parking Spot</h4>
      </div>
      <div class="card-body">
        <p class="text-muted mb-4">Reserve a parking spot for your upcoming visit.</p>

        <form @submit.prevent="submitReservation">
          <div class="mb-3">
            <label class="form-label">Parking Lot</label>
            <select v-model="form.lotId" class="form-select" required>
              <option value="">-- Select Lot --</option>
              <option v-for="lot in lots" :key="lot.lot_id" :value="lot.lot_id">
                {{ lot.prime_location_name }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label class="form-label">Spot</label>
            <select v-model="form.spotId" class="form-select" :disabled="!form.lotId || loading" required>
              <option value="">-- Select Spot --</option>
              <option v-for="spot in spots" :key="spot.id" :value="spot.id">
                {{ spot.spot_number || spot.number || spot.id }} ({{ spot.type || 'General' }})
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
            <button type="submit" class="btn btn-primary" :disabled="loading || !form.spotId">
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
import { reactive, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api'

const router = useRouter()
const lots = ref([])
const spots = ref([])
const loading = ref(false)
const error = ref('')

const form = reactive({
  lotId: '',
  spotId: '',
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

watch(() => form.lotId, async (v) => {
  spots.value = []
  form.spotId = ''
  if (!v) return
  loading.value = true
  try {
    const { data } = await api.get(`/api/lots/${v}/spots`, { params: { status: 'available' } })
    spots.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

async function submitReservation() {
  if (!form.spotId) return
  loading.value = true
  error.value = ''
  try {
    await api.post('/api/reservations', {
      lot_id: form.lotId,
      spot_id: form.spotId,
      vehicle_number: form.vehicleNumber,
      start_time: form.from,
      end_time: form.to
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
