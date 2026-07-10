<template>
  <div class="admin-page py-4">
    <div class="mb-4">
      <h4 class="page-title mb-1">Reports & Analytics</h4>
      <p class="page-subtitle text-muted mb-0">Track bookings revenue, guide allocation, and trek popularity</p>
    </div>

    <!-- Quick stats indicators -->
    <div class="row g-4 mb-4">
      <div class="col-12 col-md-4">
        <div class="metric-card">
          <span class="metric-lbl text-muted">Monthly Revenue</span>
          <h4 class="metric-val">{{ reportsData.total_revenue }}</h4>
          <span class="trend text-success"><i class="bi bi-arrow-up-short"></i> Active sales</span>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="metric-card">
          <span class="metric-lbl text-muted">Avg. Booking Value</span>
          <h4 class="metric-val">{{ reportsData.avg_booking_value }}</h4>
          <span class="trend text-success"><i class="bi bi-arrow-up-short"></i> Per traveler</span>
        </div>
      </div>
      <div class="col-12 col-md-4">
        <div class="metric-card">
          <span class="metric-lbl text-muted">Active Excursions</span>
          <h4 class="metric-val">{{ reportsData.active_excursions }}</h4>
          <span class="trend text-muted">Steady season rate</span>
        </div>
      </div>
    </div>

    <!-- Analytics Sections -->
    <div class="row g-4">
      <div class="col-12 col-lg-8">
        <div class="dashboard-panel h-100">
          <h5 class="panel-header mb-3">Trek Popularity Index</h5>
          <div class="progress-list d-flex flex-column gap-3">
            <div v-for="tp in reportsData.popularity_index" :key="tp.name">
              <div class="d-flex justify-content-between text-sm mb-1">
                <span class="fw-semibold">{{ tp.name }}</span>
                <span class="text-muted">{{ tp.count }} bookings ({{ tp.percentage }}%)</span>
              </div>
              <div class="progress-bar-container">
                <div class="progress-bar-fill" :style="{ width: tp.percentage + '%' }"></div>
              </div>
            </div>
            <div v-if="reportsData.popularity_index.length === 0" class="text-center py-4 text-secondary">
              No bookings recorded yet.
            </div>
          </div>
        </div>
      </div>

      <div class="col-12 col-lg-4">
        <div class="dashboard-panel h-100">
          <h5 class="panel-header mb-3">Trek Status Distribution</h5>
          <div class="distribution-list d-flex flex-column gap-3 mt-4">
            <div class="d-flex align-items-center justify-content-between">
              <span class="text-sm"><i class="bi bi-circle-fill text-success me-2"></i> Confirmed Bookings</span>
              <span class="fw-bold text-dark">{{ reportsData.distribution.confirmed }}% ({{ reportsData.distribution.confirmed_count || 0 }})</span>
            </div>
            <div class="d-flex align-items-center justify-content-between">
              <span class="text-sm"><i class="bi bi-circle-fill text-warning me-2"></i> Pending Approvals</span>
              <span class="fw-bold text-dark">{{ reportsData.distribution.pending }}% ({{ reportsData.distribution.pending_count || 0 }})</span>
            </div>
            <div class="d-flex align-items-center justify-content-between">
              <span class="text-sm"><i class="bi bi-circle-fill text-danger me-2"></i> Cancelled Bookings</span>
              <span class="fw-bold text-dark">{{ reportsData.distribution.cancelled }}% ({{ reportsData.distribution.cancelled_count || 0 }})</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/api.js'

const reportsData = ref({
  total_revenue: '₹0',
  avg_booking_value: '₹0',
  active_excursions: '0 Treks',
  popularity_index: [],
  distribution: {
    confirmed: 0,
    pending: 0,
    cancelled: 0,
    confirmed_count: 0,
    pending_count: 0,
    cancelled_count: 0
  }
})

const fetchReports = async () => {
  try {
    const response = await api.get('/admin/reports')
    if (response.data && response.data.success) {
      reportsData.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching reports data:', error)
  }
}

onMounted(() => {
  fetchReports()
})
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

.metric-card {
  background: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
}

.metric-lbl {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.metric-val {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  margin: 0.35rem 0;
}

.trend {
  font-size: 0.775rem;
  font-weight: 500;
}

.dashboard-panel {
  background: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 1.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
}

.panel-header {
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
}

.text-sm {
  font-size: 0.875rem;
}

/* Progress bar styles */
.progress-bar-container {
  height: 8px;
  background-color: #f3f4f6;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 4px;
}

.progress-bar-fill {
  height: 100%;
  background-color: #ff6b35;
  border-radius: 4px;
}
</style>
