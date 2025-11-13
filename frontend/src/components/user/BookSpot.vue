<template>
  <div class="book-spot">
    <h3>Book Spot</h3>
    <p>Reserve a parking spot for your upcoming visit.</p>

    <form @submit.prevent="submitReservation">
      <label>
        Lot
        <select v-model="form.lotId">
          <option disabled value="">Select lot</option>
          <option v-for="lot in lots" :key="lot.lot_id" :value="lot.lot_id">{{ lot.prime_location_name }}</option>
        </select>
      </label>

      <label>
        Spot Number
        <input v-model="form.spotId" placeholder="Eg. C-12" required />
      </label>

      <label>
        Vehicle Number
        <input v-model="form.vehicleNumber" placeholder="TN-00-AA-0000" required />
      </label>

      <div class="row">
        <label>
          Parking From
          <input v-model="form.from" type="datetime-local" required />
        </label>
        <label>
          Parking To
          <input v-model="form.to" type="datetime-local" required />
        </label>
      </div>

      <button type="submit">Reserve</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'

const lots = ref([])
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

const form = reactive({
  lotId: '',
  spotId: '',
  vehicleNumber: '',
  from: '',
  to: '',
  cost: 0
});

function submitReservation() {
  // Wire to backend later with auth.
  alert(`Reservation requested for spot ${form.spotId}`)
}
</script>

<style scoped>
.book-spot { display: flex; flex-direction: column; gap: 1rem; }
form { display: flex; flex-direction: column; gap: 1rem; max-width: 600px; }
label { display: flex; flex-direction: column; gap: 0.25rem; }
.row { display: flex; gap: 1rem; }
.row label { flex: 1; }
</style>
