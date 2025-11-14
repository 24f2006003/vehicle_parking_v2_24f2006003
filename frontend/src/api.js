import axios from 'axios'

const api = axios.create({
  // baseURL left blank; use absolute '/api' paths to leverage Vite proxy
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token && !config.headers?.Authorization) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
