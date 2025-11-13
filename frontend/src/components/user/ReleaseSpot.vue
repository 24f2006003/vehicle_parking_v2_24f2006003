<template>
  <div class="release-spot">
    <h3>Release Spot</h3>
    <p>Confirm checkout details before leaving the parking lot.</p>

    <form @submit.prevent="releaseSpot">
      <label>
        Spot Number
        <input v-model="form.spotId" required />
      </label>

      <label>
        Vehicle Number
        <input v-model="form.vehicleNumber" required />
      </label>

      <div class="row">
        <label>
          Parking Start
          <input v-model="form.from" type="datetime-local" required />
        </label>
        <label>
          Parking End
          <input v-model="form.to" type="datetime-local" required />
        </label>
      </div>

      <label>
        Payable Amount (₹)
        <input v-model.number="form.amount" type="number" min="0" step="0.5" required />
      </label>

      <label>
        Notes
        <textarea v-model="form.notes" rows="3" placeholder="Any remarks"></textarea>
      </label>

      <div class="actions">
        <button type="submit">Release</button>
        <button type="button" @click="cancel">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';

const form = reactive({
  spotId: '',
  vehicleNumber: '',
  from: '',
  to: '',
  amount: 0,
  notes: ''
});

function releaseSpot() {
  alert(`Spot ${form.spotId} released (mock).`);
}

function cancel() {
  Object.assign(form, { spotId: '', vehicleNumber: '', from: '', to: '', amount: 0, notes: '' });
}
</script>

<style scoped>
.release-spot { display: flex; flex-direction: column; gap: 1rem; }
form { display: flex; flex-direction: column; gap: 1rem; max-width: 600px; }
label { display: flex; flex-direction: column; gap: 0.25rem; }
.row { display: flex; gap: 1rem; }
.row label { flex: 1; }
.actions { display: flex; gap: 0.75rem; }
</style>
