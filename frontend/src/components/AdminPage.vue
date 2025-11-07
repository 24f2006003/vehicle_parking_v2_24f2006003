<script setup>
import { ref, onMounted } from 'vue'

const parkingLots = ref([])

const fetchParkingLots = async () => {
  try {
    const response = await fetch('/api/parking-lots')
    parkingLots.value = await response.json()
  } catch (error) {
    console.error('Error fetching parking lots:', error)
  }
}

onMounted(() => {
  fetchParkingLots()
})
</script>

<template>
  <div class="admin-container">
    <nav class="navbar">
      <div class="navbar-content">
        <span class="navbar-brand">Welcome Admin</span>
        <ul class="nav-links">
          <li><a href="#" class="active">Home</a></li>
          <li><a href="#">Summary</a></li>
          <li><a href="#">Logout</a></li>
        </ul>
      </div>
    </nav>

    <div class="content">
      <h3 class="title">Parking Lots</h3>
      
      <div class="lots-grid">
        <div v-for="lot in parkingLots" :key="lot.id" class="lot-card">
          <div class="card-header">{{ lot.name }}</div>
          <div class="card-body">
            <table class="slots-table">
              <thead>
                <tr>
                  <th>Slot Number</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="slot in lot.slots" :key="slot.id">
                  <td>{{ slot.number }}</td>
                  <td>{{ slot.status }}</td>
                  <td>
                    <button class="btn-edit">Edit</button>
                    <button class="btn-delete">Delete</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div class="card-actions">
              <button class="btn-edit">Edit</button>
              <button class="btn-primary">+ Slot</button>
              <button class="btn-delete">Delete</button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="add-lot">
        <button class="btn-primary">+ Add Lot</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: #e9ecef;
  padding: 1rem 2rem;
  border-bottom: 1px solid #dee2e6;
}

.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-weight: 600;
  font-size: 1.25rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav-links a {
  text-decoration: none;
  color: #495057;
}

.nav-links a.active {
  color: #007bff;
  font-weight: 500;
}

.content {
  padding: 2rem;
}

.title {
  text-align: center;
  margin-bottom: 2rem;
}

.lots-grid {
  display: grid;
  gap: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.lot-card {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.card-header {
  background: #f8f9fa;
  padding: 0.75rem;
  text-align: center;
  font-weight: 600;
  border-bottom: 1px solid #dee2e6;
}

.card-body {
  padding: 1rem;
}

.slots-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.slots-table th,
.slots-table td {
  padding: 0.5rem;
  text-align: left;
  border: 1px solid #dee2e6;
}

.slots-table th {
  background: #f8f9fa;
  font-weight: 600;
}

.card-actions {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.btn-edit {
  background: #ffc107;
  color: #000;
  border: none;
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-delete {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-primary {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.375rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
}

.add-lot {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.add-lot .btn-primary {
  padding: 0.5rem 1.5rem;
}
</style>