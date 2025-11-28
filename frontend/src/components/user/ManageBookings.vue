<template>
  <div class="container">
    <div class="card shadow-sm mx-auto" style="max-width: 600px;">
      <div class="card-header bg-primary text-white">
        <h4 class="mb-0">Manage Bookings</h4>
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
            <h5 class="alert-heading">Current Reservation</h5>
            <p class="mb-0">Spot ID: <strong>{{ reservation.spot_id }}</strong></p>
            <p class="mb-0">Start Time: {{ formatDate(reservation.parking_timestamp) }}</p>
            <p class="mb-0">End Time: {{ formatDate(reservation.leaving_timestamp) }}</p>
            <p class="mb-0">Status: <strong>{{ reservation.status }}</strong></p>
          </div>

          <div v-if="invoice" class="alert alert-success mt-3">
            <h4 class="alert-heading">Payment Successful!</h4>
            <p>Total Amount Paid: <strong>₹{{ invoice.amount }}</strong></p>
            <hr>
            <p class="mb-0">Thank you for parking with us.</p>
            <button class="btn btn-outline-success mt-2" @click="$router.push('/user/history')">View History</button>
          </div>

          <div v-else class="d-grid gap-2">
            <!-- Occupy Spot -->
            <button v-if="reservation.status === 'active' || reservation.status === 'reserved'"
              class="btn btn-success btn-lg" @click="occupySpot" :disabled="!canOccupy">
              Occupy Spot
            </button>
            <p v-if="!canOccupy && (reservation.status === 'active' || reservation.status === 'reserved')"
              class="text-muted small text-center">
              You can occupy the spot at the booking start time.
            </p>

            <!-- Release Spot -->
            <button v-if="reservation.status === 'occupied'" class="btn btn-danger btn-lg" @click="releaseSpot">
              Release Spot & Pay
            </button>

            <!-- Cancel Booking -->
            <button v-if="canCancel" class="btn btn-outline-secondary" @click="cancelBooking">
              Cancel Booking
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '../../api';

const reservation = ref(null);
const loading = ref(true);
const invoice = ref(null);

onMounted(async () => {
  await fetchReservation();
});

async function fetchReservation() {
  loading.value = true;
  try {
    const { data } = await api.get('/api/reservations');
    // Find active reservation (could be 'active' or 'occupied' depending on backend status)
    // Assuming 'active' means booked but not yet occupied/completed?
    // Or maybe 'active' covers both?
    // Let's check backend models. Status 'A' is Available, 'O' is Occupied (Spot).
    // Reservation status: 'active', 'L' (Left?), 'C' (Completed).
    // Wait, backend `create_reservation` sets spot status 'O'.
    // And reservation status defaults to... it's not set in `create_reservation` explicitly?
    // `Reservation` model default? I need to check `models.py`.
    // But `get_reservations` returns `status`.

    if (Array.isArray(data)) {
      // We want the current active one.
      reservation.value = data.find(r => r.status !== 'C' && r.status !== 'L' && r.status !== 'cancelled');
    }
  } catch (e) {
    console.error('Failed to load reservations', e);
  } finally {
    loading.value = false;
  }
}

function formatDate(dateString) {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString();
}

const canOccupy = computed(() => {
  if (!reservation.value) return false;
  const now = new Date();
  const start = new Date(reservation.value.parking_timestamp);
  return now >= start;
});

const canCancel = computed(() => {
  if (!reservation.value) return false;
  // Can cancel only before start time
  const now = new Date();
  const start = new Date(reservation.value.parking_timestamp);
  return now < start && reservation.value.status !== 'occupied';
});

async function occupySpot() {
  try {
    // Backend doesn't have explicit 'occupy' action yet, but let's assume 'active' -> 'occupied'
    // Actually, `create_reservation` sets spot to 'O' immediately.
    // So the spot IS occupied physically or reserved.
    // The user wants a flow: Book -> Occupy -> Release.
    // If I book for tomorrow, spot is 'O' (Reserved).
    // "Occupy" might just be a status update on Reservation to say "User Arrived".
    // Or maybe we don't need backend change if it's just visual?
    // But the user said "User should be able to checkin...".
    // I'll add an action 'occupy' to `update_reservation` in backend if needed.
    // For now, I'll use a local status or a custom action.
    // Let's assume I need to add 'occupy' action to backend.

    await api.patch(`/api/reservations/${reservation.value.reservation_id}`, {
      action: 'occupy'
    });
    alert('Spot Occupied!');
    await fetchReservation();
  } catch (e) {
    alert('Failed to occupy spot: ' + (e.response?.data?.message || e.message));
  }
}

async function releaseSpot() {
  if (!confirm('Are you sure you want to end your parking session?')) return;

  try {
    await api.patch(`/api/reservations/${reservation.value.reservation_id}`, {
      action: 'complete'
    });

    const { data } = await api.get(`/api/reservations/${reservation.value.reservation_id}/invoice`);
    invoice.value = data.invoice;
    reservation.value = null; // Clear active reservation view
  } catch (e) {
    alert('Failed to release spot: ' + (e.response?.data?.message || e.message));
  }
}

async function cancelBooking() {
  if (!confirm('Cancel this booking?')) return;
  try {
    await api.delete(`/api/reservations/${reservation.value.reservation_id}`);
    alert('Booking cancelled.');
    reservation.value = null;
  } catch (e) {
    alert('Failed to cancel: ' + (e.response?.data?.message || e.message));
  }
}
</script>
