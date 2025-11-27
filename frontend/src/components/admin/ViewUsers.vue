<template>
  <div>
    <h4 class="mb-4 border-start border-4 border-success ps-2">Registered Users</h4>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="text-danger">{{ error }}</div>

    <div v-else class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-striped table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>
                  <div class="fw-bold">{{ user.username }}</div>
                </td>
                <td>{{ user.email }}</td>
                <td>
                  <span class="badge" :class="user.role === 'admin' ? 'bg-warning text-dark' : 'bg-info'">
                    {{ user.role }}
                  </span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-primary me-1" @click="viewUser(user)">View</button>
                  <!-- Add more actions if needed -->
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

const users = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get('/api/users')
    users.value = data.users
  } catch (e) {
    error.value = 'Could not load users'
  } finally {
    loading.value = false
  }
})

function viewUser(user) {
  alert(`User Details:\nID: ${user.id}\nUsername: ${user.username}\nEmail: ${user.email}\nRole: ${user.role}`)
}
</script>
