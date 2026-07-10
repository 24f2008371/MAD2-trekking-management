<template>
  <div class="admin-page py-4">
    <div class="mb-4">
      <h4 class="page-title mb-1">Global Database Search</h4>
      <p class="page-subtitle text-muted mb-0">Search across treks, bookings, trekking staff, and users</p>
    </div>

    <div class="dashboard-panel mb-4">
      <div class="search-input-wrapper">
        <i class="bi bi-search search-icon"></i>
        <input 
          v-model="query" 
          type="text" 
          placeholder="Type user name, trek name, email, booking status, or staff role..." 
          class="search-bar"
          @input="handleSearch"
        />
      </div>
    </div>

    <!-- Results section -->
    <div v-if="results.length > 0" class="dashboard-panel">
      <h5 class="results-header mb-3">Search Results ({{ results.length }} items found)</h5>
      <div class="table-responsive">
        <table class="table align-middle custom-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Details</th>
              <th>Matches</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="res in results" :key="res.key">
              <td>
                <span class="badge-type" :class="res.type.toLowerCase()">
                  {{ res.type }}
                </span>
              </td>
              <td>
                <div class="fw-semibold text-dark">{{ res.title }}</div>
                <div class="text-muted text-sm">{{ res.subtitle }}</div>
              </td>
              <td>
                <span class="text-sm font-monospace">{{ res.matchText }}</span>
              </td>
              <td>
                <button class="btn btn-action" @click="viewDetail(res)">
                  <i class="bi bi-eye"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-else-if="query.trim().length > 0" class="dashboard-panel py-5 text-center">
      <i class="bi bi-search text-muted fs-1 mb-3 d-block"></i>
      <h5 class="text-dark">No records matched your search query</h5>
      <p class="text-muted text-sm mb-0">Try typing another keyword (e.g. 'sharma', 'pass', 'lead', or 'confirmed')</p>
    </div>
    
    <div v-else class="dashboard-panel py-5 text-center text-muted">
      <i class="bi bi-terminal fs-1 mb-3 d-block text-orange"></i>
      <h5>Waiting for search query...</h5>
      <p class="text-sm mb-0">Your query results will appear here in real-time.</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../../api/api.js'

const query = ref('')
const results = ref([])

const handleSearch = async () => {
  const q = query.value.trim()
  if (!q) {
    results.value = []
    return
  }
  
  try {
    const response = await api.get('/admin/search', {
      params: { q }
    })
    if (response.data && response.data.success) {
      results.value = response.data.data
    }
  } catch (error) {
    console.error('Error conducting search query:', error)
  }
}

const viewDetail = (res) => {
  alert(`Viewing details of ${res.type}: ${res.title}`)
}
</script>

<style scoped>
.admin-page {
  width: 100%;
}

.page-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #111827;
}

.page-subtitle {
  font-size: 0.85rem;
}

.dashboard-panel {
  background: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 1.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 18px;
  color: #9ca3af;
  font-size: 1.1rem;
}

.search-bar {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 3rem;
  border: 1px solid #eaeaea;
  border-radius: 12px;
  outline: none;
  font-size: 0.95rem;
  transition: all 0.2s;
  color: #111827;
  background-color: #fafaf9;
}

.search-bar:focus {
  border-color: #ff6b35;
  background-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

.results-header {
  font-size: 0.95rem;
  font-weight: 700;
  color: #374151;
}

.custom-table {
  width: 100%;
  margin-bottom: 0;
}

.custom-table th {
  font-size: 0.775rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 700;
  color: #6b7280;
  border-bottom: 1px solid #f3f4f6;
  padding: 0.85rem 0.75rem;
}

.custom-table td {
  padding: 0.85rem 0.75rem;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.875rem;
  color: #374151;
}

.badge-type {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.02em;
}

.badge-type.trek { background-color: #eff6ff; color: #1e40af; }
.badge-type.user { background-color: #f0fdf4; color: #166534; }
.badge-type.staff { background-color: #faf5ff; color: #6b21a8; }
.badge-type.booking { background-color: #fffbeb; color: #92400e; }

.btn-action {
  width: 28px;
  height: 28px;
  padding: 0;
  border-radius: 6px;
  border: 1px solid #eaeaea;
  background-color: #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  transition: all 0.2s;
  color: #4b5563;
}

.btn-action:hover {
  background-color: #f9fafb;
  border-color: #d1d5db;
}

.text-orange {
  color: #ff6b35;
}

.text-sm {
  font-size: 0.775rem;
}
</style>
