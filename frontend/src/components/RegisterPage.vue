<template>
  <NavPage />
  <div class="container py-3">
    <h1 class="mb-2">Create Account</h1>
    <p class="text-muted">Register to book and manage parking spots.</p>

    <form @submit.prevent="onSubmit" class="row g-3" style="max-width: 720px;">
      <div class="col-12">
        <label class="form-label">Username</label>
        <input v-model.trim="form.username" class="form-control" placeholder="e.g. arnav_01" required />
      </div>
      <div class="col-12">
        <label class="form-label">Email</label>
        <input v-model.trim="form.email" type="email" class="form-control" placeholder="you@example.com" required />
      </div>
      <div class="col-md-6">
        <label class="form-label">Password</label>
        <input v-model="form.password" type="password" class="form-control" required />
      </div>
      <div class="col-md-6">
        <label class="form-label">Confirm Password</label>
        <input v-model="form.confirm" type="password" class="form-control" required />
      </div>
      <div class="col-12 d-flex align-items-center gap-2">
        <button type="submit" class="btn btn-primary">Register</button>
        <router-link to="/login" class="btn btn-outline-secondary">Have an account? Login</router-link>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import api from '../api'
import NavPage from './NavPage.vue'

const form = reactive({ username: '', email: '', password: '', confirm: '' })

async function onSubmit() {
	if (form.password !== form.confirm) {
		alert('Passwords do not match')
		return
	}
	try {
		await api.post('/api/register', { username: form.username, email: form.email, password: form.password })
		alert('Registered successfully')
		window.location.href = '/login'
	} catch (e) {
		alert('Registration failed')
	}
}
</script>

<style scoped>

</style>
