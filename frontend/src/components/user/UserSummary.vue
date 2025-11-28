<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-4 border-start border-4 border-primary ps-3">
      <h3 class="mb-0">User Summary</h3>
      <button class="btn btn-outline-primary" @click="exportCSV" :disabled="exporting">
        <span v-if="exporting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        {{ exporting ? 'Exporting...' : 'Export as CSV' }}
      </button>
    </div>

    <!-- Alert for Export -->
    <div v-if="exportMessage" class="alert alert-success alert-dismissible fade show" role="alert">
      {{ exportMessage }}
      <button type="button" class="btn-close" @click="exportMessage = ''" aria-label="Close"></button>
    </div>

    <!-- Summary Cards -->
    <div class="row g-4 mb-5">
      <div class="col-md-4">
        <div class="card text-white bg-primary h-100 shadow-sm border-0">
          <div class="card-body">
            <h5 class="card-title opacity-75">Total Reservations</h5>
            <p class="display-4 fw-bold mb-0">{{ summary.totalReservations }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-info h-100 shadow-sm border-0">
          <div class="card-body text-white">
            <h5 class="card-title opacity-75">Hours Parked</h5>
            <p class="display-4 fw-bold mb-0">{{ summary.hoursParked }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-success h-100 shadow-sm border-0">
          <div class="card-body">
            <h5 class="card-title opacity-75">Amount Spent (₹)</h5>
            <p class="display-4 fw-bold mb-0">{{ summary.amountSpent.toFixed(2) }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Visual Charts (Bootstrap Progress Bars) -->
    <div class="row g-4">
      <div class="col-md-6">
        <div class="card h-100 shadow-sm border-0">
          <div class="card-header bg-white fw-bold py-3">Activity Overview</div>
          <div class="card-body text-center">
            <img :src="chartUrl" alt="Activity Chart" class="img-fluid" v-if="chartUrl" />
            <div v-else class="spinner-border text-primary" role="status"></div>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card h-100 shadow-sm border-0">
          <div class="card-header bg-white fw-bold py-3">Spending Analysis</div>
          <div class="card-body">
            <p class="text-muted small mb-3">Spending distribution across your top locations.</p>

            <div v-if="Object.keys(spendingByLot).length === 0" class="text-center text-muted py-4">
              No spending data available.
            </div>

            <div v-for="(amount, lotId) in spendingByLot" :key="lotId" class="mb-3">
              <div class="d-flex justify-content-between mb-1">
                <span>Lot #{{ lotId }}</span>
                <span>₹{{ amount.toFixed(2) }}</span>
              </div>
              <div class="progress" style="height: 8px;">
                <div class="progress-bar bg-info" role="progressbar"
                  :style="{ width: getSpendingPercent(amount) + '%' }" :aria-valuenow="getSpendingPercent(amount)"
                  aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api'

const summary = ref({ totalReservations: 0, hoursParked: 0, amountSpent: 0 })
const reservations = ref([])
const exporting = ref(false)
const exportMessage = ref('')
const spendingByLot = ref({})
const chartUrl = ref('')

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) return
  try {
    // Fetch Chart
    const res = await api.get('/api/charts/user_summary', { responseType: 'blob' })
    chartUrl.value = URL.createObjectURL(res.data)

    const { data } = await api.get('/api/reservations')
    reservations.value = data

    summary.value.totalReservations = data.length
    summary.value.amountSpent = data.reduce((s, r) => s + (r.parking_cost || 0), 0)
    summary.value.hoursParked = data.length * 2 // Mock: assuming avg 2 hours per booking

    // Calculate spending by lot
    const spending = {}
    data.forEach(r => {
      if (r.parking_cost) {
        spending[r.spot_id] = (spending[r.spot_id] || 0) + r.parking_cost // Using spot_id as proxy for lot if lot_id missing in this view
      }
    })
    spendingByLot.value = spending

  } catch (e) {
    console.error(e)
  }
})

async function exportCSV() {
  exporting.value = true
  exportMessage.value = ''
  try {
    exportMessage.value = 'Export started successfully.'

    // Trigger direct download
    const response = await api.get('/api/export_csv/download', { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'parking_history.csv')
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

  } catch (e) {
    exportMessage.value = 'Failed to start export or download.'
  } finally {
    exporting.value = false
  }
}

function getSpendingPercent(amount) {
  if (summary.value.amountSpent === 0) return 0
  return Math.round((amount / summary.value.amountSpent) * 100)
}
</script>
