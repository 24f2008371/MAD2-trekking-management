<template>
  <div class="admin-page py-4">
    <!-- Header Section -->
    <div class="d-flex align-items-center justify-content-between mb-4">
      <div>
        <h4 class="page-title mb-1">Treks Management</h4>
        <p class="page-subtitle text-muted mb-0">Create, edit, and monitor trekking expeditions</p>
      </div>
      <button 
        v-if="!showForm" 
        class="btn btn-primary-orange animate-fade-in" 
        @click="openAddForm"
      >
        <i class="bi bi-plus-lg me-1"></i> Add New Trek
      </button>
    </div>

    <!-- Success message banner -->
    <div v-if="successMsg" class="feedback-banner success-banner mb-4 animate-fade-in">
      <i class="bi bi-check-circle-fill me-2"></i>
      <span>{{ successMsg }}</span>
    </div>

    <!-- Add / Edit Trek Form Panel -->
    <div v-if="showForm" class="dashboard-panel mb-4 animate-fade-in">
      <h5 class="panel-section-title mb-4">
        {{ editingTrekId ? 'Edit Trek Details' : 'Create New Trek Expedition' }}
      </h5>

      <!-- Error alert -->
      <div v-if="errorMsg" class="alert alert-danger-custom mb-4">
        <i class="bi bi-exclamation-circle-fill me-2"></i> {{ errorMsg }}
      </div>

      <form @submit.prevent="handleSaveTrek">
        <div class="row g-4">
          <!-- Trek Name -->
          <div class="col-12 col-md-6">
            <label class="form-label text-sm fw-semibold">Trek Name</label>
            <input 
              v-model="form.name" 
              type="text" 
              placeholder="e.g. Everest Base Camp" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Location -->
          <div class="col-12 col-md-6">
            <label class="form-label text-sm fw-semibold">Location</label>
            <input 
              v-model="form.location" 
              type="text" 
              placeholder="e.g. Nepal or Uttarakhand" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Difficulty -->
          <div class="col-12 col-md-4">
            <label class="form-label text-sm fw-semibold">Difficulty</label>
            <select v-model="form.difficulty" class="form-select custom-input">
              <option value="Easy">Easy</option>
              <option value="Moderate">Moderate</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <!-- Duration (days) -->
          <div class="col-12 col-md-4">
            <label class="form-label text-sm fw-semibold">Duration (Days)</label>
            <input 
              v-model="form.duration" 
              type="number" 
              placeholder="e.g. 12" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Price -->
          <div class="col-12 col-md-4">
            <label class="form-label text-sm fw-semibold">Price (INR)</label>
            <input 
              v-model="form.price" 
              type="number" 
              placeholder="e.g. 48000" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Slots -->
          <div class="col-12 col-md-4">
            <label class="form-label text-sm fw-semibold">Available Slots</label>
            <input 
              v-model="form.slots" 
              type="number" 
              placeholder="e.g. 15" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Start Date -->
          <div class="col-12 col-md-4">
            <label class="form-label text-sm fw-semibold">Start Date</label>
            <input 
              v-model="form.start_date" 
              type="date" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- End Date -->
          <div class="col-12 col-md-4">
            <label class="form-label text-sm fw-semibold">End Date</label>
            <input 
              v-model="form.end_date" 
              type="date" 
              class="form-control custom-input" 
              required 
            />
          </div>

          <!-- Image Upload -->
          <div class="col-12 col-md-8">
            <label class="form-label text-sm fw-semibold">Trek Image</label>
            <div class="d-flex align-items-center gap-3">
              <input 
                type="file" 
                ref="fileInputRef" 
                class="d-none" 
                accept="image/*"
                @change="handleFileUpload" 
              />
              <button 
                type="button" 
                class="btn btn-cancel-custom d-flex align-items-center gap-2"
                @click="fileInputRef.click()"
              >
                <i class="bi bi-cloud-upload"></i> Upload Image
              </button>
              <div v-if="uploading" class="spinner-border spinner-border-sm text-orange" role="status"></div>
              <span v-if="form.image" class="text-sm text-success fw-semibold">
                Image uploaded successfully!
              </span>
            </div>
            <!-- Show a mini thumbnail preview of the uploaded or current image if available -->
            <div v-if="form.image" class="mt-3">
              <img :src="form.image" class="img-thumbnail animate-fade-in" style="max-height: 80px;" alt="Trek preview" />
            </div>
          </div>

          <!-- Status Dropdown -->
          <div class="col-12 col-md-4">
            <label class="form-label text-sm fw-semibold">Status</label>
            <select v-model="form.status" class="form-select custom-input">
              <option value="Open">Open</option>
              <option value="Closed">Closed</option>
              <option value="Completed">Completed</option>
            </select>
          </div>

          <!-- Allot Staff Guide -->
          <div class="col-12 col-md-4">
            <label class="form-label text-sm fw-semibold">Assign Staff Guide</label>
            <select v-model="form.staff_id" class="form-select custom-input">
              <option value="">Unassigned</option>
              <option v-for="s in staffList" :key="s.id" :value="s.id">
                {{ s.username }} ({{ s.specialization || 'Guide' }})
              </option>
            </select>
          </div>
        </div>

        <!-- Buttons -->
        <div class="d-flex align-items-center justify-content-end gap-3 mt-5">
          <button type="button" class="btn btn-cancel-custom" @click="resetForm">Cancel</button>
          <button type="submit" class="btn btn-create-custom" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ editingTrekId ? 'Update Trek' : 'Create Trek' }}
          </button>
        </div>
      </form>
    </div>

    <!-- Treks Table Panel -->
    <div class="dashboard-panel">
      <div class="table-responsive">
        <table class="table align-middle custom-table">
          <thead>
            <tr>
              <th>Trek Name</th>
              <th>Location</th>
              <th>Difficulty</th>
              <th>Duration</th>
              <th>Price</th>
              <th>Status</th>
              <th>Assigned Staff</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trek in treks" :key="trek.id">
              <td>
                <div class="fw-semibold text-dark">{{ trek.name }}</div>
              </td>
              <td>{{ trek.location }}</td>
              <td>
                <span class="badge-difficulty" :class="trek.difficulty.toLowerCase()">
                  {{ trek.difficulty }}
                </span>
              </td>
              <td>{{ trek.duration }} Days</td>
               <td>₹{{ Number(trek.price).toLocaleString() }}</td>
              <td>
                <span class="status-dot" :class="{ active: trek.status === 'Open' }"></span>
                {{ trek.status || 'Open' }}
              </td>
              <td>
                <span class="badge bg-light text-dark border">{{ trek.staff_name || 'Unassigned' }}</span>
              </td>
              <td>
                <div class="d-flex gap-2">
                  <button class="btn btn-action" title="Edit Trek" @click="editTrek(trek)">
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button class="btn btn-action text-danger" title="Delete Trek" @click="deleteTrek(trek.id)">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="treks.length === 0">
              <td colspan="7" class="text-center py-4 text-muted">No treks registered yet. Add one to get started!</td>
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

const treks = ref([])
const successMsg = ref('')
const staffList = ref([])
const showForm = ref(false)
const editingTrekId = ref(null)
const isSubmitting = ref(false)
const errorMsg = ref('')

const fileInputRef = ref(null)
const uploading = ref(false)

const fetchStaff = async () => {
  try {
    const response = await api.get('/admin/staff')
    if (response.data && response.data.success) {
      staffList.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching staff members:', error)
  }
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  uploading.value = true
  errorMsg.value = ''
  
  const formData = new FormData()
  formData.append('file', file)
  
  try {
    const response = await api.post('/admin/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    if (response.data && response.data.success) {
      form.value.image = response.data.url
    }
  } catch (error) {
    console.error('Error uploading file:', error)
    errorMsg.value = error.response?.data?.message || 'Failed to upload image file.'
  } finally {
    uploading.value = false
  }
}

const form = ref({
  name: '',
  location: '',
  difficulty: 'Moderate',
  duration: '',
  price: '',
  slots: '',
  start_date: '',
  end_date: '',
  image: '',
  status: 'Open',
  staff_id: ''
})

const fetchTreks = async () => {
  try {
    const response = await api.get('/admin/treks')
    if (response.data && response.data.success) {
      treks.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching admin treks:', error)
  }
}

const openAddForm = () => {
  editingTrekId.value = null
  form.value = {
    name: '',
    location: '',
    difficulty: 'Moderate',
    duration: '',
    price: '',
    slots: '',
    start_date: '',
    end_date: '',
    image: '',
    status: 'Open',
    staff_id: ''
  }
  errorMsg.value = ''
  showForm.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const editTrek = (trek) => {
  editingTrekId.value = trek.id
  form.value = {
    name: trek.name,
    location: trek.location,
    difficulty: trek.difficulty,
    duration: trek.duration,
    price: trek.price,
    slots: trek.slots,
    start_date: trek.start_date,
    end_date: trek.end_date,
    image: trek.image,
    status: trek.status || 'Open',
    staff_id: trek.staff_id || ''
  }
  errorMsg.value = ''
  showForm.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const deleteTrek = async (id) => {
  if (!confirm('Are you sure you want to delete this trek? This will also remove any bookings associated with this trek.')) {
    return
  }
  try {
    const response = await api.delete(`/admin/treks/${id}`)
    if (response.data && response.data.success) {
      await fetchTreks()
    }
  } catch (error) {
    console.error('Error deleting trek:', error)
    alert(error.response?.data?.message || 'Failed to delete trek')
  }
}

const handleSaveTrek = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  isSubmitting.value = true
  
  try {
    if (editingTrekId.value) {
      // Update
      const response = await api.put(`/admin/treks/${editingTrekId.value}`, form.value)
      if (response.data && response.data.success) {
        successMsg.value = 'Trek updated'
        setTimeout(() => {
          successMsg.value = ''
        }, 3000)
        resetForm()
        await fetchTreks()
      }
    } else {
      // Create
      const response = await api.post('/admin/treks', form.value)
      if (response.data && response.data.success) {
        successMsg.value = 'Trek created'
        setTimeout(() => {
          successMsg.value = ''
        }, 3000)
        resetForm()
        await fetchTreks()
      }
    }
  } catch (error) {
    console.error('Error saving trek:', error)
    errorMsg.value = error.response?.data?.message || 'Failed to save trek details'
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  form.value = {
    name: '',
    location: '',
    difficulty: 'Moderate',
    duration: '',
    price: '',
    slots: '',
    start_date: '',
    end_date: '',
    image: '',
    status: 'Open',
    staff_id: ''
  }
  editingTrekId.value = null
  errorMsg.value = ''
  showForm.value = false
}

onMounted(async () => {
  await fetchTreks()
  await fetchStaff()
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

/* Table Style */
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

.badge-difficulty {
  display: inline-block;
  padding: 0.2rem 0.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 6px;
  text-transform: capitalize;
}

.badge-difficulty.easy {
  background-color: #f0fdf4;
  color: #166534;
}

.badge-difficulty.moderate {
  background-color: #fffbeb;
  color: #b45309;
}

.badge-difficulty.hard {
  background-color: #fef2f2;
  color: #991b1b;
}

.status-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ef4444;
  margin-right: 6px;
}

.status-dot.active {
  background-color: #22c55e;
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
  color: #4b5563;
}

.btn-action:hover {
  background-color: #f9fafb;
  border-color: #d1d5db;
  transform: translateY(-1px);
}

/* Animations */
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Banner system */
.feedback-banner {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.success-banner {
  background: #F0FDF4;
  border: 1px solid #86EFAC;
  color: #166534;
}
</style>
