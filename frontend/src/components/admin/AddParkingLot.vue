<template>
  <div class="container py-4">
    <div class="card shadow-sm mx-auto" style="max-width: 800px;">
      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Add Parking Lot</h4>
      </div>
      <div class="card-body">
        <p class="text-muted mb-4">Capture essential details to make a new parking location available.</p>

        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label class="form-label">Prime Location Name</label>
            <input v-model="form.primeLocation" type="text" class="form-control" required
              placeholder="e.g. Downtown Plaza" />
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <textarea v-model="form.address" class="form-control" rows="3" required
              placeholder="Full street address"></textarea>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Pin Code</label>
              <input v-model="form.pinCode" type="text" class="form-control" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">Price / Hour</label>
              <div class="input-group">
                <span class="input-group-text">$</span>
                <input v-model.number="form.price" type="number" class="form-control" min="0" step="0.5" required />
              </div>
            </div>
          </div>

          <div class="row mb-4">
            <div class="col-md-6">
              <label class="form-label">Total Spots</label>
              <input v-model.number="form.totalSpots" type="number" class="form-control" min="1" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">Available Spots</label>
              <input v-model.number="form.availableSpots" type="number" class="form-control" min="0" required />
            </div>
          </div>

          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button type="button" class="btn btn-secondary me-md-2" @click="$router.back()">Cancel</button>
            <button type="submit" class="btn btn-primary">Add Lot</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import api from '../../api'; // Assuming we might want to hook this up later, but keeping mock for now as per file content
import { useRouter } from 'vue-router';

const router = useRouter();
const form = reactive({
  primeLocation: '',
  address: '',
  pinCode: '',
  price: 0,
  totalSpots: 0,
  availableSpots: 0
});

async function submitForm() {
  try {
    await api.post('/api/lots', form)
    alert(`Lot ${form.primeLocation} added!`);
    router.push('/admin/view');
  } catch (e) {
    alert('Failed to add lot: ' + (e.response?.data?.message || e.message));
  }
}
</script>
