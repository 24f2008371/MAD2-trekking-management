<template>
  <div class="admin-page py-4">
    <!-- Header Section -->
    <div class="d-flex align-items-center justify-content-between mb-4">
      <div>
        <h4 class="page-title mb-1">Trekking Staff</h4>
        <p class="page-subtitle text-muted mb-0">Manage guides, mountain coordinators, and safety staff</p>
      </div>
      <button 
        v-if="!showCreateForm" 
        class="btn btn-primary-orange animate-fade-in" 
        @click="showCreateForm = true"
      >
        <i class="bi bi-plus-lg me-1"></i> Add New Staff
      </button>
    </div>

    <!-- Screen 5: Create New Trekking Staff Form -->
    <div v-if="showCreateForm" class="dashboard-panel animate-fade-in">
      <h5 class="panel-section-title mb-4">Create New Trekking Staff</h5>
      
      <!-- Error and Success Banners -->
      <div v-if="errorMsg" class="alert alert-danger-custom mb-4">
        <i class="bi bi-exclamation-circle-fill me-2"></i> {{ errorMsg }}
      </div>
      
      <form @submit.prevent="handleCreateStaff">
        <div class="row g-4">
          <!-- Full Name -->
          <div class="col-12 col-md-6">
            <label class="form-label text-sm fw-semibold">Full Name</label>
            <input 
              v-model="form.username" 
              type="text" 
              placeholder="e.g. Vikas Singh" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Email Address -->
          <div class="col-12 col-md-6">
            <label class="form-label text-sm fw-semibold">Email Address</label>
            <input 
              v-model="form.email" 
              type="email" 
              placeholder="e.g. vikas@gmail.com" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Contact Number -->
          <div class="col-12 col-md-6">
            <label class="form-label text-sm fw-semibold">Contact Number</label>
            <input 
              v-model="form.phone" 
              type="text" 
              placeholder="e.g. 9876543210" 
              class="form-control custom-input" 
            />
          </div>

          <!-- Password -->
          <div class="col-12 col-md-6">
            <label class="form-label text-sm fw-semibold">Password</label>
            <input 
              v-model="form.password" 
              type="password" 
              placeholder="••••••••" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Confirm Password -->
          <div class="col-12 col-md-6">
            <label class="form-label text-sm fw-semibold">Confirm Password</label>
            <input 
              v-model="form.confirmPassword" 
              type="password" 
              placeholder="••••••••" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Experience -->
          <div class="col-12 col-md-6">
            <label class="form-label text-sm fw-semibold">Experience (e.g., 5 years)</label>
            <input 
              v-model="form.experience" 
              type="text" 
              placeholder="e.g. 5 years" 
              class="form-control custom-input" 
            />
          </div>

          <!-- Specialization -->
          <div class="col-12 col-md-12">
            <label class="form-label text-sm fw-semibold">Specialization (e.g., High Altitude, First Aid)</label>
            <input 
              v-model="form.specialization" 
              type="text" 
              placeholder="e.g. High Altitude Rescue, Wilderness First Aid" 
              class="form-control custom-input" 
            />
          </div>

        </div>

        <!-- Buttons -->
        <div class="d-flex align-items-center justify-content-end gap-3 mt-5">
          <button type="button" class="btn btn-cancel-custom" @click="resetForm">Cancel</button>
          <button type="submit" class="btn btn-create-custom" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
            Create Staff
          </button>
        </div>
      </form>

      <!-- Footer Info Info Banner -->
      <div class="info-footer-note d-flex align-items-center mt-4">
        <i class="bi bi-info-circle-fill text-blue me-2"></i>
        <span>The staff will receive email with login credentials.</span>
      </div>
    </div>

    <!-- Screen 6: Manage Trekking Staff List -->
    <div v-else class="dashboard-panel animate-fade-in">
      <div class="d-flex align-items-center justify-content-between mb-4">
        <h5 class="panel-section-title mb-0">Trekking Staff List</h5>
      </div>

      <!-- Search Box -->
      <div class="search-wrapper mb-4">
        <i class="bi bi-search search-icon"></i>
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Search trekking staff..." 
          class="form-control search-bar" 
        />
      </div>

      <!-- Staff List Table -->
      <div class="table-responsive">
        <table class="table align-middle custom-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Contact</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="member in filteredStaff" :key="member.id">
              <td>
                <span class="staff-id-text font-monospace">TS{{ String(member.id).padStart(3, '0') }}</span>
              </td>
              <td>
                <div class="fw-semibold text-dark">{{ member.username }}</div>
                <div class="text-muted text-xs">{{ member.specialization || 'General Guide' }}</div>
              </td>
              <td>{{ member.email }}</td>
              <td>{{ member.phone || 'N/A' }}</td>
              <td>
                <span 
                  class="status-pill-badge" 
                  :class="member.status === 'blacklisted' ? 'blacklisted' : 'active'"
                >
                  {{ member.status === 'blacklisted' ? 'Blacklisted' : 'Active' }}
                </span>
              </td>
              <td>
                <button 
                  v-if="member.status !== 'blacklisted'" 
                  class="btn btn-blacklist-action" 
                  @click="toggleStaffStatus(member.id, 'blacklisted')"
                >
                  Blacklist
                </button>
                <button 
                  v-else 
                  class="btn btn-whitelist-action" 
                  @click="toggleStaffStatus(member.id, 'active')"
                >
                  Whitelist
                </button>
              </td>
            </tr>
            <tr v-if="filteredStaff.length === 0">
              <td colspan="6" class="text-center py-4 text-muted">No trekking staff members found.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Footer Info Info Banner -->
      <div class="info-footer-note d-flex align-items-center mt-4">
        <i class="bi bi-info-circle-fill text-blue me-2"></i>
        <span>Blacklisted staff cannot login or access the system.</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../../api/api.js'

const showCreateForm = ref(false)
const searchQuery = ref('')
const isSubmitting = ref(false)
const errorMsg = ref('')

const staff = ref([])

const form = ref({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  experience: '',
  specialization: '',
  status: 'active'
})

const filteredStaff = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) return staff.value
  return staff.value.filter(s => {
    return s.username.toLowerCase().includes(query) || 
           s.email.toLowerCase().includes(query) ||
           (s.phone && s.phone.includes(query))
  })
})

const fetchStaff = async () => {
  try {
    const response = await api.get('/admin/staff')
    if (response.data && response.data.success) {
      staff.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching trekking staff:', error)
  }
}

const toggleStaffStatus = async (id, newStatus) => {
  try {
    const response = await api.put(`/admin/staff/${id}/status`, {
      status: newStatus
    })
    if (response.data && response.data.success) {
      await fetchStaff()
    }
  } catch (error) {
    console.error('Error toggling staff status:', error)
    alert(error.response?.data?.message || 'Failed to update staff status')
  }
}

const handleCreateStaff = async () => {
  errorMsg.value = ''
  if (form.value.password !== form.value.confirmPassword) {
    errorMsg.value = 'Passwords do not match'
    return
  }
  
  isSubmitting.value = true
  try {
    const response = await api.post('/admin/staff', {
      username: form.value.username,
      email: form.value.email,
      phone: form.value.phone,
      password: form.value.password,
      experience: form.value.experience,
      specialization: form.value.specialization,
      status: form.value.status
    })
    if (response.data && response.data.success) {
      resetForm()
      await fetchStaff()
    }
  } catch (error) {
    console.error('Error creating staff:', error)
    errorMsg.value = error.response?.data?.message || 'Failed to create staff member'
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  form.value = {
    username: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    experience: '',
    specialization: '',
    status: 'active'
  }
  errorMsg.value = ''
  showCreateForm.value = false
}

onMounted(() => {
  fetchStaff()
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
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
}

.panel-section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #111827;
}

.custom-input {
  border: 1px solid #eaeaea;
  border-radius: 10px;
  font-size: 0.9rem;
  padding: 0.65rem 0.85rem;
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
  padding: 0.55rem 1.25rem;
  border-radius: 10px;
  font-size: 0.875rem;
  transition: opacity 0.2s;
}

.btn-primary-orange:hover {
  opacity: 0.9;
}

.btn-cancel-custom {
  background-color: #ffffff;
  border: 1px solid #eaeaea;
  color: #4b5563;
  font-weight: 600;
  padding: 0.6rem 1.5rem;
  border-radius: 10px;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.btn-cancel-custom:hover {
  background-color: #fafaf9;
  border-color: #d1d5db;
}

.btn-create-custom {
  background-color: #ff6b35;
  color: #ffffff;
  font-weight: 600;
  border: none;
  padding: 0.6rem 1.5rem;
  border-radius: 10px;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.btn-create-custom:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-create-custom:disabled {
  opacity: 0.7;
}

/* Alert styles */
.alert-danger-custom {
  background-color: #fef2f2;
  border: 1px solid #fca5a5;
  color: #991b1b;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
}

/* Search Box styles */
.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 14px;
  color: #9ca3af;
  font-size: 0.95rem;
}

.search-bar {
  padding-left: 2.5rem;
  background-color: #fafaf9;
  border: 1px solid #eaeaea;
  border-radius: 10px;
  font-size: 0.9rem;
  height: 42px;
}

.search-bar:focus {
  border-color: #ff6b35;
  background-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
}

/* Table styles */
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
  background-color: #fafaf9;
}

.custom-table td {
  padding: 0.85rem 0.75rem;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.875rem;
  color: #374151;
}

.staff-id-text {
  color: #6b7280;
  font-weight: 500;
}

/* Custom Status Badges matching screenshot outline style */
.status-pill-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.2rem 0.65rem;
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 6px;
  text-transform: capitalize;
  border: 1.5px solid transparent;
}

.status-pill-badge.active {
  border-color: #22c55e;
  color: #166534;
  background-color: #f0fdf4;
}

.status-pill-badge.blacklisted {
  border-color: #ef4444;
  color: #991b1b;
  background-color: #fef2f2;
}

/* Custom Blacklist / Whitelist buttons matching screenshot */
.btn-blacklist-action {
  background-color: #ffffff;
  color: #ef4444;
  border: 1.5px solid #ef4444;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.btn-blacklist-action:hover {
  background-color: #ef4444;
  color: #ffffff;
}

.btn-whitelist-action {
  background-color: #ffffff;
  color: #22c55e;
  border: 1.5px solid #22c55e;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.btn-whitelist-action:hover {
  background-color: #22c55e;
  color: #ffffff;
}

/* Info Note Banner */
.info-footer-note {
  background-color: #eff6ff;
  border-radius: 10px;
  padding: 0.85rem 1.25rem;
  font-size: 0.85rem;
  color: #1e3a8a;
  font-weight: 500;
}

.text-xs {
  font-size: 0.75rem;
}
.text-sm {
  font-size: 0.875rem;
}
</style>
