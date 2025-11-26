<template>
  <div class="container py-4">
    <div class="card shadow-sm mx-auto" style="max-width: 600px;">
      <div class="card-header bg-secondary text-white">
        <h4 class="mb-0">Add Parking Spots</h4>
      </div>
      <div class="card-body">
        <p class="text-muted mb-4">Extend capacity for lot #{{ lotId }} by creating new spot identifiers.</p>

        <form @submit.prevent="addSpot">
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">Start Number</label>
              <input v-model.number="batch.start" type="number" class="form-control" min="1" required />
            </div>
            <div class="col-md-6">
              <label class="form-label">Count</label>
              <input v-model.number="batch.count" type="number" class="form-control" min="1" required />
            </div>
          </div>

          <div class="mb-4">
            <label class="form-label">Spot Type</label>
            <select v-model="batch.type" class="form-select">
              <option value="general">General</option>
              <option value="ev">EV Charging</option>
              <option value="accessible">Accessible</option>
            </select>
          </div>

          <div class="d-grid gap-2 d-md-flex justify-content-md-end">
            <button type="button" class="btn btn-secondary me-md-2" @click="$router.back()">Cancel</button>
            <button type="submit" class="btn btn-primary">Generate Spots</button>
          </div>
        </form>

        <div v-if="generatedSpots.length > 0" class="mt-4">
          <h5 class="border-bottom pb-2">Generated Spots Preview</h5>
          <div class="d-flex flex-wrap gap-2 mt-2">
            <span v-for="spot in generatedSpots" :key="spot" class="badge bg-light text-dark border">
              Spot {{ spot }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import api from '../../api';

const route = useRoute();
const lotId = route.params.lot_id;

const batch = ref({
  start: 1,
  count: 5,
  type: 'general'
});

const generatedSpots = ref([]);

async function addSpot() {
  // Generate preview
  generatedSpots.value = Array.from({ length: batch.value.count }, (_, i) => `#${batch.value.start + i}`);

  try {
    await api.post(`/api/lots/${lotId}/spots`, batch.value)
    alert(`${batch.value.count} spots generated!`);
  } catch (e) {
    alert('Failed to add spots: ' + (e.response?.data?.message || e.message));
  }
}
</script>
