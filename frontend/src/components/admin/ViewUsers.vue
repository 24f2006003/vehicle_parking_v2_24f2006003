<template>
  <div>
    <h2>Registered Users</h2>
    <p>Monitor accounts.</p>

    <p v-if="loading">Loading...</p>
    <p v-if="error">{{ error }}</p>

    <table v-if="!loading && !error">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Email</th>
          <th>Role</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.role }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api'

const users = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { loading.value = false; error.value = 'Please login'; return }
  try {
    const { data } = await api.get('/api/users')
    users.value = data
  } catch (e) {
    error.value = 'Could not load users'
  } finally {
    loading.value = false
  }
})
</script>
