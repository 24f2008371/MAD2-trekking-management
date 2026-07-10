<template>
  <div class="admin-dashboard-container py-4">
    <!-- Header Summary -->
    <div class="row g-4 mb-4">
      <!-- Total Treks Card -->
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="stat-card treks-card">
          <div class="d-flex align-items-center justify-content-between mb-3">
            <span class="stat-title text-muted">Total Treks</span>
            <div class="icon-box treks-bg">
              <i class="bi bi-compass"></i>
            </div>
          </div>
          <h3 class="stat-value text-treks mb-0">{{ stats.total_treks }}</h3>
          <p class="stat-desc text-muted mb-0 mt-2">Active treks this season</p>
        </div>
      </div>

      <!-- Total Users Card -->
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="stat-card users-card">
          <div class="d-flex align-items-center justify-content-between mb-3">
            <span class="stat-title text-muted">Total Users</span>
            <div class="icon-box users-bg">
              <i class="bi bi-people"></i>
            </div>
          </div>
          <h3 class="stat-value text-users mb-0">{{ stats.total_users }}</h3>
          <p class="stat-desc text-muted mb-0 mt-2">Registered trekkers</p>
        </div>
      </div>

      <!-- Total Trekking Staff Card -->
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="stat-card staff-card">
          <div class="d-flex align-items-center justify-content-between mb-3">
            <span class="stat-title text-muted">Total Staff</span>
            <div class="icon-box staff-bg">
              <i class="bi bi-person-badge"></i>
            </div>
          </div>
          <h3 class="stat-value text-staff mb-0">{{ stats.total_staff }}</h3>
          <p class="stat-desc text-muted mb-0 mt-2">Certified local guides & staff</p>
        </div>
      </div>

      <!-- Total Bookings Card -->
      <div class="col-12 col-sm-6 col-xl-3">
        <div class="stat-card bookings-card">
          <div class="d-flex align-items-center justify-content-between mb-3">
            <span class="stat-title text-muted">Total Bookings</span>
            <div class="icon-box bookings-bg">
              <i class="bi bi-journal-check"></i>
            </div>
          </div>
          <h3 class="stat-value text-bookings mb-0">{{ stats.total_bookings }}</h3>
          <p class="stat-desc text-muted mb-0 mt-2">Booked excursions overall</p>
        </div>
      </div>
    </div>

    <!-- Recent Bookings Table Panel -->
    <div class="dashboard-panel">
      <div class="panel-header d-flex flex-wrap align-items-center justify-content-between gap-3 mb-4">
        <div>
          <h4 class="panel-title mb-1">Recent Bookings</h4>
          <p class="panel-subtitle text-muted mb-0">Real-time trekking reservations log</p>
        </div>
        <router-link to="/admin/bookings" class="btn btn-view-all">
          View All Bookings <i class="bi bi-arrow-right-short ms-1"></i>
        </router-link>
      </div>

      <div class="table-responsive">
        <table class="table align-middle custom-table">
          <thead>
            <tr>
              <th scope="col">Booking ID</th>
              <th scope="col">User</th>
              <th scope="col">Trek</th>
              <th scope="col">Booking Date</th>
              <th scope="col">Status</th>
              <th scope="col">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in bookings" :key="booking.id">
              <td>
                <span class="booking-id font-monospace">{{ booking.id }}</span>
              </td>
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="avatar-sm">
                    {{ (booking.user || '').trim().charAt(0).toUpperCase() }}
                  </div>
                  <div>
                    <div class="user-name">{{ booking.user }}</div>
                    <div class="user-email text-muted">{{ booking.email }}</div>
                  </div>
                </div>
              </td>
              <td>
                <span class="trek-name">{{ booking.trek }}</span>
              </td>
              <td>
                <span class="booking-date">{{ booking.date }}</span>
              </td>
              <td>
                <span class="status-badge" :class="booking.status ? booking.status.toLowerCase() : 'pending'">
                  {{ booking.status }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-2">
                  <button class="btn btn-action text-success" title="Approve booking" @click="handleAction(booking, 'Confirmed')">
                    <i class="bi bi-check-lg"></i>
                  </button>
                  <button class="btn btn-action text-danger" title="Cancel booking" @click="handleAction(booking, 'Cancelled')">
                    <i class="bi bi-x-lg"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../../api/api.js'

const stats = ref({
  total_treks: 34,
  total_users: 1248,
  total_staff: 42,
  total_bookings: 382
})

const bookings = ref([])

const fetchStats = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  try {
    const response = await api.get('/admin/stats', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (response.data && response.data.success) {
      stats.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching admin stats:', error)
  }
}

const fetchBookings = async () => {
  try {
    const response = await api.get('/admin/bookings')
    if (response.data && response.data.success) {
      bookings.value = response.data.data.slice(0, 5)
    }
  } catch (error) {
    console.error('Error fetching bookings:', error)
  }
}

const handleAction = async (booking, actionStatus) => {
  try {
    const response = await api.put(`/admin/bookings/${booking.raw_id}/status`, {
      status: actionStatus
    })
    if (response.data && response.data.success) {
      await fetchBookings()
      await fetchStats()
    }
  } catch (error) {
    console.error('Error updating booking status:', error)
    alert(error.response?.data?.message || 'Failed to update booking status')
  }
}

onMounted(() => {
  fetchStats()
  fetchBookings()
})
</script>

<style scoped>
/* Stat Cards */
.stat-card {
  background: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 1.5rem;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  border-radius: 4px 0 0 4px;
}

.stat-card.treks-card::before { background-color: #ff6b35; }
.stat-card.users-card::before { background-color: #3b82f6; }
.stat-card.staff-card::before { background-color: #22c55e; }
.stat-card.bookings-card::before { background-color: #a855f7; }

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.04);
  border-color: #d1d5db;
}

.stat-title {
  font-size: 0.825rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
}

.icon-box {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.treks-bg { background-color: #fff0eb; color: #ff6b35; }
.users-bg { background-color: #eff6ff; color: #3b82f6; }
.staff-bg { background-color: #f0fdf4; color: #22c55e; }
.bookings-bg { background-color: #faf5ff; color: #a855f7; }

.stat-value {
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.stat-value.text-treks { color: #ff6b35; }
.stat-value.text-users { color: #3b82f6; }
.stat-value.text-staff { color: #22c55e; }
.stat-value.text-bookings { color: #a855f7; }

.stat-desc {
  font-size: 0.8rem;
}

/* Dashboard Panel */
.dashboard-panel {
  background: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 1.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
}

.panel-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #111827;
}

.panel-subtitle {
  font-size: 0.85rem;
}

.btn-view-all {
  border: 1px solid #eaeaea;
  color: #4b5563;
  background-color: #ffffff;
  font-size: 0.875rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s;
}

.btn-view-all:hover {
  background-color: #f9fafb;
  border-color: #d1d5db;
  color: #111827;
}

/* Custom Table Styles */
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
  padding: 1rem 0.75rem;
}

.custom-table td {
  padding: 1rem 0.75rem;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.875rem;
  color: #374151;
}

.booking-id {
  color: #6b7280;
  font-weight: 500;
}

.avatar-sm {
  width: 32px;
  height: 32px;
  background-color: #ff6b35;
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.user-name {
  font-weight: 600;
  color: #111827;
}

.user-email {
  font-size: 0.775rem;
}

.trek-name {
  font-weight: 500;
  color: #111827;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.625rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 30px;
}

.status-badge.confirmed {
  background-color: #f0fdf4;
  color: #166534;
}

.status-badge.pending {
  background-color: #fffbeb;
  color: #b45309;
}

.status-badge.cancelled {
  background-color: #fef2f2;
  color: #991b1b;
}

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
}

.btn-action:hover {
  background-color: #f9fafb;
  border-color: #d1d5db;
  transform: translateY(-1px);
}
</style>
