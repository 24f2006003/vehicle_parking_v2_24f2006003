<template>
  <div class="container">
    <div class="card shadow-sm mx-auto" style="max-width: 600px;">
      <div class="card-header bg-danger text-white">
        <h4 class="mb-0">Release Spot</h4>
      </div>
      <div class="card-body">
        <div v-if="loading" class="text-center py-4">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
        </div>

        <div v-else-if="!reservation" class="text-center py-4">
          <p class="text-muted">You do not have any active parking reservations.</p>
          <router-link to="/user/book/0" class="btn btn-primary">Book a Spot</router-link>
        </div>

        <div v-else>
          <div class="alert alert-info">
            <h5 class="alert-heading">Active Session</h5>
            <p class="mb-0">Spot ID: <strong>{{ reservation.spot_id }}</strong></p>
            <p class="mb-0">Started: {{ formatDate(reservation.parking_timestamp) }}</p>
          </div>

          <div v-if="invoice" class="alert alert-success mt-3">
            <h4 class="alert-heading">Payment Successful!</h4>
            <p>Total Amount Paid: <strong>${{ invoice.amount }}</strong></p>
            <hr>
            <p class="mb-0">Thank you for parking with us.</p>
            <button class="btn btn-outline-success mt-2" @click="$router.push('/user/history')">View History</button>
          </div>

          <form v-else @submit.prevent="releaseSpot">
            <p class="text-muted mb-4">Click below to end your parking session. The final price will be calculated based
              on the duration.</p>

            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <button type="submit" class="btn btn-danger btn-lg w-100">End Parking & Pay</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../../api';

const reservation = ref(null);
const loading = ref(true);
const invoice = ref(null);

onMounted(async () => {
  try {
    const { data } = await api.get('/api/reservations');
    // Find active reservation
    if (Array.isArray(data)) {
      reservation.value = data.find(r => r.status === 'active');
    }
  } catch (e) {
    console.error('Failed to load reservations', e);
  } finally {
    loading.value = false;
  }
});

function formatDate(dateString) {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString();
}

async function releaseSpot() {
  if (!confirm('Are you sure you want to end your parking session?')) return;

  try {
    // 1. Complete the reservation
    await api.patch(`/api/reservations/${reservation.value.reservation_id}`, {
      action: 'complete'
    });

    // 2. Fetch the updated reservation to get the cost (or invoice endpoint)
    // The backend update might not return the full object, so let's fetch invoice or the reservation again.
    // Let's use the invoice endpoint if available or just get the reservation.
    // Based on routes.py, we have /api/reservations/<id>/invoice

    const { data } = await api.get(`/api/reservations/${reservation.value.reservation_id}/invoice`);
    invoice.value = data.invoice;

  } catch (e) {
    alert('Failed to release spot: ' + (e.response?.data?.message || e.message));
  }
}
</script>
