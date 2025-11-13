<template>
  <div class="add-spots panel">
    <h2>Add Parking Spots</h2>
    <p>Extend capacity for lot #{{ lotId }} by creating new spot identifiers.</p>

    <form @submit.prevent="addSpot">
      <div class="row">
        <label>
          Start Number
          <input v-model.number="batch.start" type="number" min="1" required />
        </label>
        <label>
          Count
          <input v-model.number="batch.count" type="number" min="1" required />
        </label>
      </div>
      <label>
        Spot Type
        <select v-model="batch.type">
          <option value="general">General</option>
          <option value="ev">EV Charging</option>
          <option value="accessible">Accessible</option>
        </select>
      </label>
      <button type="submit">Generate Spots</button>
    </form>

    <section class="preview">
      <h3>Generated Spots</h3>
      <p v-if="generatedSpots.length === 0">Nothing generated yet.</p>
      <ul v-else>
        <li v-for="spot in generatedSpots" :key="spot">Spot {{ spot }}</li>
      </ul>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const lotId = route.params.lot_id;

const batch = ref({
  start: 1,
  count: 5,
  type: 'general'
});

const generatedSpots = ref([]);

function addSpot() {
  generatedSpots.value = Array.from({ length: batch.value.count }, (_, i) => `#${batch.value.start + i}`);
}
</script>

<style scoped>
.panel { padding: 1rem; max-width: 520px; }
form { display: flex; flex-direction: column; gap: 0.75rem; }
label { display: flex; flex-direction: column; gap: 0.25rem; }
.row { display: flex; gap: 1rem; }
.row label { flex: 1; }
.preview { margin-top: 1rem; padding: 0.5rem; border: 1px dashed; }
</style>
