<template>
    <main>
        <section>
            <h1>Vehicle Parking System</h1>
            <p>
                <router-link to="/login">Login</router-link>
                |
                <router-link to="/register">Register</router-link>
            </p>
        </section>

    </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const lots = ref([])
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
</script>

<style scoped>
main { padding: 1rem; }
ul { padding-left: 1rem; }
li { margin-bottom: 0.5rem; }
</style>