<template>
    <footer class="footer">
        <p>
            © 2025 Vehicle Parking System ·
            <router-link to="/">Home</router-link>
            ·
            <router-link to="/login">Login</router-link>
            ·
            <router-link to="/register">Register</router-link>
        </p>
    </footer>
  
</template>

<script setup>
// Lightweight footer component for layout
</script>

<style scoped>
.footer { margin-top: 2rem; padding: 1rem; text-align: center; }
a { text-decoration: none; }
</style>