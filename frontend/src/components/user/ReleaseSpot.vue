<template>
  <div class="container">
    <div class="card shadow-sm mx-auto" style="max-width: 600px;">
      <div class="card-header bg-danger text-white">
        <h4 class="mb-0">Release Spot</h4>
      </div>
      <div class="card-body">
        <p class="text-muted mb-4">Confirm checkout details before leaving the parking lot.</p>

        <form @submit.prevent="releaseSpot">
          <div class="mb-3">
            <label class="form-label">Spot Number</label>
            <input v-model="form.spotId" type="text" class="form-control" required placeholder="e.g. #12" />
          </div>

          <div class="mb-3">
            <label class="form-label">Vehicle Number</label>
            <input v-model="form.vehicleNumber" type="text" class="form-control" required />
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Parking Start</label>
              <input v-model="form.from" type="datetime-local" class="form-control" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">Parking End</label>
              <input v-model="form.to" type="datetime-local" class="form-control" required />
            </div>
          </div>

          <div class="mb-3">
            <label class="form-label">Payable Amount (₹)</label>
            <div class="input-group">
              <span class="input-group-text">₹</span>
              <input v-model.number="form.amount" type="number" class="form-control" min="0" step="0.5" required />
            </div>
          </div>

          <div class="mb-4">
            <label class="form-label">Notes</label>
            <textarea v-model="form.notes" class="form-control" rows="3" placeholder="Any remarks"></textarea>
          </div>

          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button type="button" class="btn btn-secondary me-md-2" @click="cancel">Clear</button>
            <button type="submit" class="btn btn-danger">Release Spot</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '../../api';

const form = reactive({
  spotId: '',
  vehicleNumber: '',
  from: '',
  to: '',
  amount: 0,
  notes: ''
});

async function releaseSpot() {
  try {
    await api.post('/api/release', {
      spot_id: form.spotId,
      vehicle_number: form.vehicleNumber,
      amount: form.amount,
      notes: form.notes
    })
    alert(`Spot ${form.spotId} released successfully.`);
    // Reset form
    Object.assign(form, { spotId: '', vehicleNumber: '', from: '', to: '', amount: 0, notes: '' });
  } catch (e) {
    alert('Failed to release spot: ' + (e.response?.data?.message || e.message));
  }
}

function cancel() {
  Object.assign(form, { spotId: '', vehicleNumber: '', from: '', to: '', amount: 0, notes: '' });
}
</script>
