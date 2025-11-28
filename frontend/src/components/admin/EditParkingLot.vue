<template>
  <div class="container py-4">
    <div class="card shadow-sm mx-auto" style="max-width: 800px;">
      <div class="card-header bg-warning text-dark">
        <h4 class="mb-0">Edit Parking Lot</h4>
      </div>
      <div class="card-body">
        <p class="text-muted mb-4">Update the location details for lot #{{ lotId }}.</p>

        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label class="form-label">Prime Location Name</label>
            <input v-model="form.prime_location_name" type="text" class="form-control" required />
          </div>

          <div class="mb-3">
            <label class="form-label">Address</label>
            <textarea v-model="form.address" class="form-control" rows="3" required></textarea>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Pin Code</label>
              <input v-model="form.pin_code" type="text" class="form-control" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">Price / Hour</label>
              <div class="input-group">
                <span class="input-group-text">₹</span>
                <input v-model.number="form.price" type="number" class="form-control" min="0" step="0.5" required />
              </div>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Total Spots</label>
              <input v-model.number="form.number_of_spots" type="number" class="form-control" min="1" required />
            </div>
          </div>

          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button type="button" class="btn btn-secondary me-md-2" @click="$router.back()">Cancel</button>
            <button type="submit" class="btn btn-primary">Save Changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../../api';

const route = useRoute();
const router = useRouter();
const lotId = route.params.id;

const form = reactive({
  prime_location_name: '',
  address: '',
  pin_code: '',
  price: 0,
  number_of_spots: 0,
  available_spots: 0
});

onMounted(async () => {
  // Try to fetch existing data
  try {
    const { data } = await api.get(`/api/lots/${lotId}`)
    // Map API data to form
    form.prime_location_name = data.prime_location_name
    form.address = data.address
    form.pin_code = data.pin_code
    form.price = data.price
    form.number_of_spots = data.number_of_spots
    form.available_spots = data.available_spots
  } catch (e) {
    console.error('Failed to load lot data', e)
  }
})

async function submitForm() {
  try {
    await api.patch(`/api/lots/${lotId}`, form)
    alert(`Lot ${lotId} updated!`);
    router.push('/admin/view');
  } catch (e) {
    alert('Update failed: ' + (e.response?.data?.message || e.message));
  }
}
</script>
