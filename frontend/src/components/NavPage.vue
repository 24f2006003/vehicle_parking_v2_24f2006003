<template>
    <header class="nav">
        <div class="brand">
            <router-link to="/">Vehicle Parking</router-link>
        </div>
        <nav class="links">
            <router-link to="/">Home</router-link>
            <router-link to="/login">Login</router-link>
            <router-link to="/register">Register</router-link>
        </nav>
    </header>
</template>

<script setup>
</script>

<style scoped>
.nav { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.5rem 1rem; }
.brand a { font-weight: 700; text-decoration: none; }
.links { display: flex; gap: 0.5rem; }
.links a { text-decoration: none; padding: 0.25rem 0.5rem; }
</style>