<template>
  <div class="edit-lot panel">
    <h2>Edit Parking Lot</h2>
    <p>Update the location details for lot #{{ lotId }}.</p>

    <form @submit.prevent="submitForm">
      <label>
        Prime Location Name
        <input v-model="form.primeLocation" required />
      </label>

      <label>
        Address
        <textarea v-model="form.address" rows="3" required></textarea>
      </label>

      <div class="row">
        <label>
          Pin Code
          <input v-model="form.pinCode" required />
        </label>
        <label>
          Price / Hour
          <input v-model.number="form.price" type="number" min="0" step="0.5" required />
        </label>
      </div>

      <div class="row">
        <label>
          Number of Spots
          <input v-model.number="form.totalSpots" type="number" min="1" required />
        </label>
        <label>
          Available Spots
          <input v-model.number="form.availableSpots" type="number" min="0" required />
        </label>
      </div>

      <div class="row">
        <label>
          Occupied Spots
          <input v-model.number="form.occupiedSpots" type="number" min="0" required />
        </label>
        <label>
          Status
          <select v-model="form.status">
            <option value="active">Active</option>
            <option value="maintenance">Maintenance</option>
          </select>
        </label>
      </div>

      <button type="submit">Save Changes</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const lotId = route.params.id;

const form = reactive({
  primeLocation: 'Default Central Parking',
  address: '42 Sample Road, Demo City',
  pinCode: '600001',
  price: 25,
  totalSpots: 120,
  availableSpots: 48,
  occupiedSpots: 72,
  status: 'active'
});

function submitForm() {
  alert(`Lot ${lotId} updated (mock).`);
}
</script>

<style scoped>
.panel { padding: 1rem; max-width: 680px; }
form { display: flex; flex-direction: column; gap: 0.75rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; }
.row { display: flex; gap: 1rem; }
.row label { flex: 1; }
</style>
