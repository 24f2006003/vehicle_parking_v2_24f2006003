<template>
  <div class="book-spot">
    <h3>Book Spot</h3>
    <p>Reserve a parking spot for your upcoming visit.</p>

    <form @submit.prevent="submitReservation">
      <script setup>
      import { ref, onMounted, watch } from 'vue'
      import api from '../../api'

      const lots = ref([])
      const spots = ref([])
      const selectedLot = ref('')
      const loading = ref(true)
      const error = ref('')

      onMounted(async () => {
        try {
          const { data } = await api.get('/api/lots')
          lots.value = data
        } catch (e) {
          error.value = 'Could not load lots'
        } finally {
          loading.value = false
        }
      })

      watch(selectedLot, async (v) => {
        spots.value = []
        if (!v) return
        try {
          const { data } = await api.get(`/api/lots/${selectedLot.value}/spots`)
          spots.value = data
        } catch (e) {
          error.value = 'Could not load spots'
        }
      })
      </script>

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
