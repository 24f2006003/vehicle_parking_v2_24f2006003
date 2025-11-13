<template>
	<div class="register-page">
		<section>
			<h1>Create Account</h1>
			<p class="sub">Register to book and manage parking spots.</p>

			<form @submit.prevent="onSubmit" class="simple-form">
				<label>
					Username
					<input v-model.trim="form.username" placeholder="e.g. arnav_01" required />
				</label>

				<label>
					Email
					<input v-model.trim="form.email" type="email" placeholder="you@example.com" required />
				</label>

				<div class="row">
					<label>
						Password
						<input v-model="form.password" type="password" required />
					</label>
					<label>
						Confirm Password
						<input v-model="form.confirm" type="password" required />
					</label>
				</div>

				<div class="actions">
					<button type="submit">Register</button>
					<router-link to="/login">Have an account? Login</router-link>
				</div>
			</form>
		</section>
	</div>
  
</template>

<script setup>
import { reactive } from 'vue'

const form = reactive({ username: '', email: '', password: '', confirm: '' })

async function onSubmit() {
	if (form.password !== form.confirm) {
		alert('Passwords do not match')
		return
	}
	try {
		const res = await fetch('/api/register', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ username: form.username, email: form.email, password: form.password })
		})
		if (!res.ok) {
			alert('Registration failed')
			return
		}
		alert('Registered successfully')
		window.location.href = '/login'
	} catch (e) {
		alert('Network error')
	}
}
</script>

<style scoped>
.register-page { padding: 1rem; }
.simple-form { display: flex; flex-direction: column; gap: 0.75rem; max-width: 600px; }
label { display: flex; flex-direction: column; gap: 0.25rem; }
.row { display: flex; gap: 0.75rem; }
.row label { flex: 1; }
.actions { display: flex; gap: 0.75rem; align-items: center; }
</style>
