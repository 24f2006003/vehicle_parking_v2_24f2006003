<template>
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4 border-start border-4 border-primary ps-3">
            <h3 class="mb-0">User Details</h3>
            <button class="btn btn-outline-secondary" @click="$router.push('/admin/users')">Back to Users</button>
        </div>

        <div v-if="loading" class="text-center py-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

        <div v-else>
            <!-- User Info Card -->
            <div class="card shadow-sm mb-4">
                <div class="card-header bg-light fw-bold">User Information</div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-4">
                            <p class="mb-1 text-muted">User ID</p>
                            <p class="fw-bold">{{ user.id }}</p>
                        </div>
                        <div class="col-md-4">
                            <p class="mb-1 text-muted">Username</p>
                            <p class="fw-bold">{{ user.username }}</p>
                        </div>
                        <div class="col-md-4">
                            <p class="mb-1 text-muted">Email</p>
                            <p class="fw-bold">{{ user.email }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Reservation History -->
            <h5 class="mb-3">Reservation History</h5>
            <div class="card shadow-sm">
                <div class="card-body p-0">
                    <div class="table-responsive">
                        <table class="table table-striped table-hover mb-0">
                            <thead class="table-light">
                                <tr>
                                    <th>ID</th>
                                    <th>Lot ID</th>
                                    <th>Spot ID</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-if="reservations.length === 0">
                                    <td colspan="4" class="text-center py-3 text-muted">No reservations found.</td>
                                </tr>
                                <tr v-for="res in reservations" :key="res.id">
                                    <td>{{ res.id }}</td>
                                    <td>{{ res.lot_id }}</td>
                                    <td>{{ res.spot_id }}</td>
                                    <td>
                                        <span class="badge" :class="getStatusClass(res.status)">{{ res.status }}</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
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
const user = ref({})
const reservations = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    const userId = route.params.id
    try {
        const [userRes, historyRes] = await Promise.all([
            api.get(`/api/users/${userId}`),
            api.get(`/api/users/${userId}/reservations`)
        ])
        user.value = userRes.data.user
        reservations.value = historyRes.data.reservations
    } catch (e) {
        error.value = 'Could not load user details'
        console.error(e)
    } finally {
        loading.value = false
    }
})

function getStatusClass(status) {
    switch (status) {
        case 'active': return 'bg-success'
        case 'completed': return 'bg-secondary'
        case 'cancelled': return 'bg-danger'
        default: return 'bg-info'
    }
}
</script>
