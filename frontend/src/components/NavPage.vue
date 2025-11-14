<template>
    <nav class="navbar navbar-expand bg-light px-3">
        <a href="#" class="navbar-brand" @click.prevent="goHome">Vehicle Parking</a>
        <div class="ms-auto d-flex align-items-center gap-2">
            <a href="#" class="btn btn-sm btn-outline-secondary" @click.prevent="goHome">Home</a>
            <template v-if="!isLoggedIn">
                <router-link class="btn btn-sm btn-primary" to="/login">Login</router-link>
                <router-link class="btn btn-sm btn-outline-secondary" to="/register">Register</router-link>
            </template>
            <template v-else>
                <button class="btn btn-sm btn-danger" @click="logout">Logout</button>
            </template>
        </div>
    </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()
const isLoggedIn = ref(false)
const isAdmin = ref(false)

function refreshAuthFlags() {
    const token = localStorage.getItem('token')
    isLoggedIn.value = !!token
}

async function detectRole() {
    const token = localStorage.getItem('token')
    if (!token) { isAdmin.value = false; return }
    try {
        await api.get('/api/admin_home')
        isAdmin.value = true
    } catch {
        isAdmin.value = false
    }
}

function goHome() {
    if (!isLoggedIn.value) { router.push('/') ; return }
    if (isAdmin.value) { router.push('/admin'); return }
    router.push('/user')
}

function logout() {
    localStorage.removeItem('token')
    refreshAuthFlags()
    isAdmin.value = false
    router.push('/')
}

onMounted(() => {
    refreshAuthFlags()
    detectRole()
    window.addEventListener('storage', () => { refreshAuthFlags(); detectRole() })
})
</script>

<style scoped>

</style>