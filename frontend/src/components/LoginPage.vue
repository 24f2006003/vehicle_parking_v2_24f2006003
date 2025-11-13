<script>
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
        const res = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.formData)
        });
        if (!res.ok) {
          this.error = 'Login failed';
          return;
        }
        const data = await res.json();
        localStorage.setItem('token', data.access_token);
        this.$router.push('/');
      } catch (e) {
        this.error = 'Network error';
      }
    }
  }
}
</script>

<template>
  <div class="login-page">
    <section>
      <h1>Login</h1>
      <form @submit.prevent="loginUser" class="simple-form">
        <label>
          Email
          <input type="email" v-model="formData.email" required />
        </label>
        <label>
          Password
          <input type="password" v-model="formData.password" required />
        </label>
        <div class="actions">
          <button type="submit">Login</button>
          <router-link to="/register">Register</router-link>
        </div>
        <p v-if="error">{{ error }}</p>
      </form>
    </section>
  </div>
</template>

<style scoped>
.login-page { padding: 1rem; }
.simple-form { display: flex; flex-direction: column; gap: 0.75rem; max-width: 600px; }
label { display: flex; flex-direction: column; gap: 0.25rem; }
.actions { display: flex; gap: 0.75rem; align-items: center; }
</style>
