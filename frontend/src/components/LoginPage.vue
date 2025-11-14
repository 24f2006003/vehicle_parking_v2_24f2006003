<script>
import api from '../api'
export default {
  data() {
    return {
      formData: { email: "", password: "" },
      error: ""
    }
  },
  methods: {
    async loginUser() {
      this.error = "";
      try {
        const { data } = await api.post('/api/login', this.formData)
        localStorage.setItem('token', data.access_token)
        try {
          await api.get('/api/admin_home')
          this.$router.push('/admin')
        } catch {
          this.$router.push('/user')
        }
      } catch (e) {
        this.error = 'Login failed'
      }
    }
  }
}
</script>

<template>
  <div class="container py-3">
    <h1 class="mb-3">Login</h1>
    <form @submit.prevent="loginUser" class="row g-3" style="max-width: 640px;">
      <div class="col-12">
        <label class="form-label">Email</label>
        <input type="email" v-model="formData.email" required class="form-control" />
      </div>
      <div class="col-12">
        <label class="form-label">Password</label>
        <input type="password" v-model="formData.password" required class="form-control" />
      </div>
      <div class="col-12 d-flex align-items-center gap-2">
        <button type="submit" class="btn btn-primary">Login</button>
        <router-link to="/register" class="btn btn-outline-secondary">Register</router-link>
      </div>
      <p v-if="error" class="text-danger mt-2 mb-0">{{ error }}</p>
    </form>
  </div>
</template>

<style scoped>

</style>
