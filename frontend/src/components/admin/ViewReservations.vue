<template>
    <div>
        <h4 class="mb-4 border-start border-4 border-primary ps-2">All Reservations</h4>

        <div v-if="loading">Loading...</div>
        <div v-else-if="error" class="text-danger">{{ error }}</div>

        <div v-else class="card shadow-sm">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-striped table-hover mb-0">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Spot ID</th>
                                <th>Lot ID</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="res in reservations" :key="res.id">
                                <td>{{ res.id }}</td>
                                <td>{{ res.spot_id }}</td>
                                <td>{{ res.lot_id }}</td>
                                <td>
                                    <span class="badge" :class="getStatusClass(res.status)">
                                        {{ res.status }}
                                    </span>
                                </td>
                                <td>
                                    <!-- Add actions if needed, e.g., cancel -->
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const reservations = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    try {
        const { data } = await api.get('/api/reservations')
        reservations.value = data.reservations
    } catch (e) {
        error.value = 'Could not load reservations'
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
