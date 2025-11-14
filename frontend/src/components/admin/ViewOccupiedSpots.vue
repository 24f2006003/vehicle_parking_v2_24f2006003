<template>
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import api from '../../api'

  const lots = ref([])
  const selectedLot = ref('')
  const spots = ref([])
  const loading = ref(true)
  const error = ref('')

  onMounted(async () => {
    try {
      const { data } = await api.get('/api/lots')
      lots.value = data
    } catch (e) {
      error.value = 'Could not load lots'
    } finally {
      loading.value = false
    }
  })

  watch(selectedLot, async (v) => {
    spots.value = []
    if (!v) return
    try {
      const { data } = await api.get(`/api/lots/${selectedLot.value}/spots`, { params: { status: 'O' } })
      spots.value = data
    } catch (e) {
      error.value = 'Could not load spots'
    }
  })
  </script>
import { ref, onMounted } from 'vue'

const lots = ref([])
const spots = ref([])
const selectedLot = ref(0)
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    const res = await fetch('/api/lots')
    if (!res.ok) throw new Error()
    lots.value = await res.json()
  } catch (e) {
    error.value = 'Could not load lots'
  }
})

async function loadSpots() {
  if (!selectedLot.value) return
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`/api/lots/${selectedLot.value}/spots?status=O`)
    if (!res.ok) throw new Error()
    spots.value = await res.json()
  } catch (e) {
    error.value = 'Could not load spots'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
th, td { border: 1px solid; padding: 0.5rem; text-align: left; }
</style>
