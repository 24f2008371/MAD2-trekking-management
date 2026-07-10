<template>
  <div class="admin-page py-4">
    <div class="mb-4">
      <h4 class="page-title mb-1">Bookings Register</h4>
      <p class="page-subtitle text-muted mb-0">Review, approve, and manage all trek bookings</p>
    </div>

    <div class="dashboard-panel">
      <div class="table-responsive">
        <table class="table align-middle custom-table">
          <thead>
            <tr>
              <th>Booking ID</th>
              <th>User</th>
              <th>Trek</th>
              <th>Booking Date</th>
              <th>Status</th>
              <th>Action</th>
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

const bookings = ref([])

const fetchBookings = async () => {
  try {
    const response = await api.get('/admin/bookings')
    if (response.data && response.data.success) {
      bookings.value = response.data.data
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
    }
  } catch (error) {
    console.error('Error updating booking status:', error)
    alert(error.response?.data?.message || 'Failed to update booking status')
  }
}

onMounted(() => {
  fetchBookings()
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

.dashboard-panel {
  background: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 1.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
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
