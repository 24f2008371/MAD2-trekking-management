<template>
  <div class="admin-page py-4">
    <div class="mb-4">
      <h4 class="page-title mb-1">System Settings</h4>
      <p class="page-subtitle text-muted mb-0">Configure TrekMate portal, booking rules, and account info</p>
    </div>

    <div class="row g-4">
      <!-- Form Configurations -->
      <div class="col-12 col-lg-7">
        <div class="dashboard-panel mb-4">
          <h5 class="panel-header mb-4">Portal Configuration</h5>
          <form @submit.prevent="saveSettings">
            <div class="mb-3">
              <label class="form-label text-sm fw-semibold">Application Name</label>
              <input type="text" class="form-control custom-input" v-model="appName" />
            </div>
            
            <div class="mb-3">
              <label class="form-label text-sm fw-semibold">Support Email Address</label>
              <input type="email" class="form-control custom-input" v-model="supportEmail" />
            </div>

            <div class="mb-3">
              <label class="form-label text-sm fw-semibold">Booking Window Limit (Days)</label>
              <input type="number" class="form-control custom-input" v-model="bookingLimit" />
              <div class="form-text text-xs text-muted">Minimum number of days in advance a user must book a trek.</div>
            </div>

            <button type="submit" class="btn btn-primary-orange mt-2">
              Save Settings
            </button>
          </form>
        </div>
      </div>

      <!-- Quick Info / Help -->
      <div class="col-12 col-lg-5">
        <div class="dashboard-panel">
          <h5 class="panel-header mb-3">System Information</h5>
          <div class="d-flex flex-column gap-3">
            <div class="info-item">
              <span class="info-label text-muted d-block text-xs">Framework Version</span>
              <span class="info-value fw-semibold">Vue 3.x + Vite</span>
            </div>
            <div class="info-item">
              <span class="info-label text-muted d-block text-xs">Styling Foundation</span>
              <span class="info-value fw-semibold">Bootstrap 5.3</span>
            </div>
            <div class="info-item">
              <span class="info-label text-muted d-block text-xs">Database Connectivity</span>
              <span class="info-value fw-semibold text-success"><span class="status-dot"></span> Backend Active</span>
            </div>
            <hr class="my-2" />
            <div class="info-item">
              <span class="info-label text-muted d-block text-xs">Current Session Role</span>
              <span class="info-value badge-role">ADMINISTRATOR</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const appName = ref('TrekMate Admin Panel')
const supportEmail = ref('admin@trekmate.com')
const bookingLimit = ref(7)

const saveSettings = () => {
  alert('Settings saved successfully (Backend placeholder).')
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

.panel-header {
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
}

.custom-input {
  border: 1px solid #eaeaea;
  border-radius: 10px;
  font-size: 0.9rem;
  padding: 0.6rem 0.85rem;
  background-color: #fafaf9;
  outline: none;
  transition: all 0.2s;
}

.custom-input:focus {
  border-color: #ff6b35;
  background-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

.btn-primary-orange {
  background-color: #ff6b35;
  color: #ffffff;
  font-weight: 600;
  border: none;
  padding: 0.55rem 1.35rem;
  border-radius: 10px;
  font-size: 0.875rem;
  transition: opacity 0.2s;
}

.btn-primary-orange:hover {
  opacity: 0.9;
}

.text-sm {
  font-size: 0.875rem;
}

.text-xs {
  font-size: 0.775rem;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #22c55e;
  margin-right: 4px;
}

.badge-role {
  font-size: 0.725rem;
  font-weight: 700;
  background-color: #fff0eb;
  color: #ff6b35;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  letter-spacing: 0.05em;
  display: inline-block;
}
</style>
