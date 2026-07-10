<template>
  <div class="admin-page py-4">
    <div class="mb-4">
      <h4 class="page-title mb-1">Users (Trekkers)</h4>
      <p class="page-subtitle text-muted mb-0">Monitor registered users, active profiles, and login status</p>
    </div>

    <!-- Active Trekkers Panel -->
    <div class="dashboard-panel mb-5">
      <h5 class="panel-section-title mb-3">Active & Suspended Trekkers</h5>
      <div class="table-responsive">
        <table class="table align-middle custom-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in activeUsers" :key="user.id">
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="avatar-sm">
                    {{ (user.username || '').trim().charAt(0).toUpperCase() }}
                  </div>
                  <div class="fw-semibold text-dark">{{ (user.username || '').trim() }}</div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>{{ user.phone || 'N/A' }}</td>
              <td>
                <span class="status-badge" :class="user.status ? user.status.toLowerCase() : 'active'">
                  {{ user.status || 'Active' }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-2">
                  <button class="btn btn-action text-danger" @click="blacklistUser(user.id)" title="Blacklist User">
                    <i class="bi bi-shield-slash"></i> Blacklist
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="activeUsers.length === 0">
              <td colspan="5" class="text-center py-4 text-muted">No active users found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Blacklisted Trekkers Panel -->
    <div class="dashboard-panel">
      <h5 class="panel-section-title mb-3 text-danger"><i class="bi bi-exclamation-octagon-fill me-1"></i> Blacklisted Trekkers</h5>
      <div class="table-responsive">
        <table class="table align-middle custom-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in blacklistedUsers" :key="user.id">
              <td>
                <div class="d-flex align-items-center gap-2">
                  <div class="avatar-sm bg-danger-subtle text-danger">
                    {{ (user.username || '').trim().charAt(0).toUpperCase() }}
                  </div>
                  <div class="fw-semibold text-dark">{{ (user.username || '').trim() }}</div>
                </div>
              </td>
              <td>{{ user.email }}</td>
              <td>{{ user.phone || 'N/A' }}</td>
              <td>
                <span class="status-badge blacklisted">
                  {{ user.status }}
                </span>
              </td>
              <td>
                <div class="d-flex gap-2">
                  <button class="btn btn-action text-success" @click="unblacklistUser(user.id)" title="Unblacklist User">
                    <i class="bi bi-shield-check"></i> Unblacklist
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="blacklistedUsers.length === 0">
              <td colspan="5" class="text-center py-4 text-muted">No blacklisted users.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api/api.js'

const users = ref([])

const activeUsers = computed(() => {
  return users.value.filter(u => u.status !== 'blacklisted')
})

const blacklistedUsers = computed(() => {
  return users.value.filter(u => u.status === 'blacklisted')
})

const fetchUsers = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  try {
    const response = await api.get('/admin/users', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (response.data && response.data.success) {
      users.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

const updateStatus = async (userId, newStatus) => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  try {
    const response = await api.put(`/admin/users/${userId}/status`, {
      status: newStatus
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (response.data && response.data.success) {
      // Refresh local list
      await fetchUsers()
    }
  } catch (error) {
    console.error('Error updating user status:', error)
    alert(error.response?.data?.message || 'Failed to update user status')
  }
}

const blacklistUser = (id) => {
  updateStatus(id, 'blacklisted')
}

const unblacklistUser = (id) => {
  updateStatus(id, 'active')
}

onMounted(() => {
  fetchUsers()
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

.panel-section-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: #374151;
  text-transform: uppercase;
  letter-spacing: 0.03em;
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

.avatar-sm.bg-danger-subtle {
  background-color: #fef2f2 !important;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.625rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 30px;
  text-transform: capitalize;
}

.status-badge.active {
  background-color: #f0fdf4;
  color: #166534;
}

.status-badge.suspended {
  background-color: #fffbeb;
  color: #b45309;
}

.status-badge.blacklisted {
  background-color: #fef2f2;
  color: #991b1b;
}

.btn-action {
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #eaeaea;
  background-color: #ffffff;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  transition: all 0.2s;
  color: #374151;
}

.btn-action:hover {
  background-color: #f9fafb;
  border-color: #d1d5db;
  transform: translateY(-1px);
}
</style>
