<template>
    <div>
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="border-start border-4 border-primary ps-2">Reservation Details</h4>
            <button class="btn btn-outline-secondary" @click="$router.go(-1)">
                <i class="bi bi-arrow-left"></i> Back
            </button>
        </div>

        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

        <div v-else class="card shadow-sm">
            <div class="card-header bg-light">
                <h5 class="mb-0">Reservation #{{ reservation.id }}</h5>
            </div>
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-6">
                        <label class="form-label text-muted">User</label>
                        <p class="fw-bold">{{ reservation.username }} (ID: {{ reservation.user_id }})</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Vehicle Number</label>
                        <p class="fw-bold">{{ reservation.vehicle_number || 'N/A' }}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Parking Lot</label>
                        <p class="fw-bold">{{ reservation.lot_name }} (ID: {{ reservation.lot_id }})</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Spot ID</label>
                        <p class="fw-bold">{{ reservation.spot_id }}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Parking Time</label>
                        <p class="fw-bold">{{ formatDate(reservation.parking_timestamp) }}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Leaving Time</label>
                        <p class="fw-bold">{{ formatDate(reservation.leaving_timestamp) || 'Ongoing' }}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Cost</label>
                        <p class="fw-bold">₹{{ reservation.parking_cost || 0 }}</p>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label text-muted">Status</label>
                        <span class="badge" :class="getStatusClass(reservation.status)">
                            {{ reservation.status }}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../../api'

const route = useRoute()
const reservation = ref({})
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    try {
        const { data } = await api.get(`/api/reservations/${route.params.id}`)
        reservation.value = data
    } catch (e) {
        error.value = 'Could not load reservation details'
    } finally {
        loading.value = false
    }
})

function formatDate(dateStr) {
    if (!dateStr) return null
    return new Date(dateStr).toLocaleString()
}

function getStatusClass(status) {
    switch (status) {
        case 'active': return 'bg-success'
        case 'completed': return 'bg-secondary'
        case 'cancelled': return 'bg-danger'
        default: return 'bg-info'
    }
}
</script>
