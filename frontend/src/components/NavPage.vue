<template>
    <header class="navbar navbar-expand bg-light px-3">
        <a href="#" class="navbar-brand" @click.prevent="goHome">Vehicle Parking</a>
        <div class="ms-auto">
            <ul class="navbar-nav align-items-center">
                <li class="nav-item">
                    <a href="#" class="nav-link" @click.prevent="goHome">Home</a>
                </li>
                <template v-if="!isLoggedIn">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/login">Login</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/register">Register</router-link>
                    </li>
                </template>
                <template v-else>
                    <li class="nav-item">
                        <a href="#" class="nav-link" @click.prevent="logout">Logout</a>
                    </li>
                </template>
            </ul>
        </div>
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

</style>