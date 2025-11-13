<template>
    <header class="nav">
        <div class="brand">
            <a href="#" @click.prevent="goHome">Vehicle Parking</a>
        </div>
        <nav class="links">
            <a href="#" @click.prevent="goHome">Home</a>
            <template v-if="!isLoggedIn">
                <router-link to="/login">Login</router-link>
                <router-link to="/register">Register</router-link>
            </template>
            <template v-else>
                <a href="#" @click.prevent="logout">Logout</a>
            </template>
        </nav>
    </header>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

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
        const res = await fetch('/api/admin_home', { headers: { Authorization: `Bearer ${token}` } })
        isAdmin.value = res.ok
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
.nav { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.5rem 1rem; }
.brand a { font-weight: 700; text-decoration: none; }
.links { display: flex; gap: 0.5rem; }
.links a { text-decoration: none; padding: 0.25rem 0.5rem; }
</style>