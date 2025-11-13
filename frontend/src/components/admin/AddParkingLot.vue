<template>
  <div class="add-lot panel">
    <h2>Add Parking Lot</h2>
    <p>Capture essential details to make a new parking location available.</p>

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

      <button type="submit">Add Lot</button>
    </form>

    <section class="preview">
      <h3>Preview</h3>
      <ul>
        <li><strong>Location:</strong> {{ form.primeLocation }}</li>
        <li><strong>Address:</strong> {{ form.address }}</li>
        <li><strong>Pin Code:</strong> {{ form.pinCode }}</li>
        <li><strong>Rate:</strong> ₹ {{ form.price.toFixed(2) }}</li>
        <li><strong>Spots:</strong> {{ form.availableSpots }} / {{ form.totalSpots }}</li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { reactive } from 'vue';

const form = reactive({
  primeLocation: '',
  address: '',
  pinCode: '',
  price: 0,
  totalSpots: 0,
  availableSpots: 0
});

function submitForm() {
  // Placeholder handler
  alert(`Lot ${form.primeLocation || 'Unnamed'} saved (mock).`);
}
</script>

<style scoped>
.panel { padding: 1rem; max-width: 640px; }
form { display: flex; flex-direction: column; gap: 0.75rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; }
.row { display: flex; gap: 1rem; }
.row label { flex: 1; }
.preview { margin-top: 1rem; padding: 0.5rem; border: 1px dashed; }
</style>
