<template>
  <div class="dashboard-wrapper">
    <!-- Collapsible Sidebar -->
    <aside class="sidebar">
      <router-link to="/" class="sidebar-brand text-decoration-none">
        <span class="logo-text">Trek<span class="orange-text">Mate</span></span>
        <span class="logo-badge">Staff</span>
      </router-link>

      <nav class="sidebar-nav mt-4">
        <a href="#" class="nav-item" :class="{ active: currentTab === 'dashboard' }" @click.prevent="currentTab = 'dashboard'">
          <span class="nav-icon"><i class="bi bi-grid"></i></span>
          <span class="nav-label">Dashboard</span>
        </a>
        <a href="#" class="nav-item" :class="{ active: currentTab === 'treks' }" @click.prevent="currentTab = 'treks'">
          <span class="nav-icon"><i class="bi bi-compass"></i></span>
          <span class="nav-label">My Treks</span>
        </a>
        <a href="#" class="nav-item" :class="{ active: currentTab === 'profile' }" @click.prevent="currentTab = 'profile'">
          <span class="nav-icon"><i class="bi bi-person"></i></span>
          <span class="nav-label">Profile</span>
        </a>
      </nav>

      <div class="sidebar-footer">
        <a href="#" class="nav-item logout-btn" @click.prevent="handleLogout">
          <span class="nav-icon"><i class="bi bi-box-arrow-right"></i></span>
          <span class="nav-label">Logout</span>
        </a>
      </div>
    </aside>

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Top Header Bar -->
      <header class="top-bar">
        <div class="welcome-message">
          <span class="app-subtitle text-muted">Trekking Management Application</span>
        </div>
        <div class="top-bar-actions">
          <div class="profile-dropdown">
            <div class="profile-trigger">
              <div class="avatar-placeholder">S</div>
              <span class="username">{{ username }}</span>
            </div>
          </div>
        </div>
      </header>

      <!-- TAB: Dashboard -->
      <div v-if="currentTab === 'dashboard'" class="tab-content animate-fade-in">
        <div class="d-flex align-items-center justify-content-between mb-4">
          <h4 class="page-title mb-0">My Dashboard</h4>
        </div>

        <!-- Metric Stat Cards -->
        <div class="row g-4 mb-4">
          <!-- Assigned Treks -->
          <div class="col-12 col-md-4">
            <div class="stat-card blue-card d-flex align-items-center justify-content-between">
              <div>
                <span class="stat-title text-muted d-block mb-1">Assigned Treks</span>
                <h3 class="stat-value text-blue mb-0">{{ stats.assigned_treks }}</h3>
              </div>
              <div class="stat-icon-box blue-bg">
                <i class="bi bi-calendar-event"></i>
              </div>
            </div>
          </div>

          <!-- Total Participants -->
          <div class="col-12 col-md-4">
            <div class="stat-card green-card d-flex align-items-center justify-content-between">
              <div>
                <span class="stat-title text-muted d-block mb-1">Total Participants</span>
                <h3 class="stat-value text-green mb-0">{{ stats.total_participants }}</h3>
              </div>
              <div class="stat-icon-box green-bg">
                <i class="bi bi-people"></i>
              </div>
            </div>
          </div>

          <!-- Ongoing Treks -->
          <div class="col-12 col-md-4">
            <div class="stat-card orange-card d-flex align-items-center justify-content-between">
              <div>
                <span class="stat-title text-muted d-block mb-1">Ongoing Treks</span>
                <h3 class="stat-value text-orange mb-0">{{ stats.ongoing_treks }}</h3>
              </div>
              <div class="stat-icon-box orange-bg">
                <i class="bi bi-map"></i>
              </div>
            </div>
          </div>
        </div>

        <!-- Assigned Treks Table Panel -->
        <div class="dashboard-panel">
          <h5 class="panel-section-title mb-4">My Assigned Treks</h5>
          <div v-if="assignedTreks.length === 0" class="text-center py-4 text-secondary">
            <p class="mb-0">No treks assigned to you yet.</p>
          </div>
          <div v-else class="table-responsive">
            <table class="table align-middle custom-table">
              <thead>
                <tr>
                  <th>Trek Name</th>
                  <th>Dates</th>
                  <th>Participants</th>
                  <th>Slots</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="trek in assignedTreks" :key="trek.id">
                  <td>
                    <div class="fw-semibold text-dark">{{ trek.name }}</div>
                  </td>
                  <td>{{ trek.dates }}</td>
                  <td>{{ trek.participants }}</td>
                  <td>{{ trek.slots }}</td>
                  <td>
                    <span class="status-pill" :class="trek.status.toLowerCase()">
                      {{ trek.status }}
                    </span>
                  </td>
                  <td>
                    <button 
                      class="btn" 
                      :class="trek.status === 'Open' ? 'btn-manage-action' : 'btn-view-action'"
                      @click="handleTrekAction(trek)"
                    >
                      {{ trek.status === 'Open' ? 'Manage' : 'View' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TAB: My Treks List (Same as dashboard treks table) -->
      <div v-else-if="currentTab === 'treks'" class="tab-content animate-fade-in">
        <div class="d-flex align-items-center justify-content-between mb-4">
          <h4 class="page-title mb-0">My Assigned Treks</h4>
        </div>
        <div class="dashboard-panel">
          <div class="table-responsive">
            <table class="table align-middle custom-table">
              <thead>
                <tr>
                  <th>Trek Name</th>
                  <th>Dates</th>
                  <th>Participants</th>
                  <th>Slots</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="trek in assignedTreks" :key="trek.id">
                  <td>
                    <div class="fw-semibold text-dark">{{ trek.name }}</div>
                  </td>
                  <td>{{ trek.dates }}</td>
                  <td>{{ trek.participants }}</td>
                  <td>{{ trek.slots }}</td>
                  <td>
                    <span class="status-pill" :class="trek.status.toLowerCase()">
                      {{ trek.status }}
                    </span>
                  </td>
                  <td>
                    <button 
                      class="btn" 
                      :class="trek.status === 'Open' ? 'btn-manage-action' : 'btn-view-action'"
                      @click="handleTrekAction(trek)"
                    >
                      {{ trek.status === 'Open' ? 'Manage' : 'View' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- TAB: Manage Selected Trek Detail -->
      <div v-else-if="currentTab === 'manage_trek'" class="tab-content animate-fade-in">
        <div class="mb-4">
          <a href="#" class="text-decoration-none text-orange fw-bold d-inline-flex align-items-center gap-1 mb-2 text-sm" @click.prevent="currentTab = 'treks'">
            <i class="bi bi-arrow-left"></i> Back to My Treks
          </a>
          <h4 class="page-title mb-0">Manage Expedition: {{ selectedTrek.name }}</h4>
        </div>

        <div class="row g-4">
          <!-- Left details panel -->
          <div class="col-12 col-lg-5">
            <div class="dashboard-panel h-100 p-4">
              <h5 class="panel-section-title mb-4 border-bottom pb-2">Trek Details</h5>
              
              <div class="d-flex flex-column gap-3 mb-4">
                <div class="d-flex justify-content-between">
                  <span class="text-secondary fw-semibold">Destination:</span>
                  <span class="fw-bold text-dark">{{ selectedTrek.location }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-secondary fw-semibold">Difficulty:</span>
                  <span class="fw-bold text-dark">{{ selectedTrek.difficulty }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-secondary fw-semibold">Duration:</span>
                  <span class="fw-bold text-dark">{{ selectedTrek.duration }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-secondary fw-semibold">Start Date:</span>
                  <span class="fw-bold text-dark">{{ selectedTrek.start_date }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-secondary fw-semibold">End Date:</span>
                  <span class="fw-bold text-dark">{{ selectedTrek.end_date }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-secondary fw-semibold">Total Slots:</span>
                  <span class="fw-bold text-dark">{{ selectedTrek.total_slots }}</span>
                </div>
                <div class="d-flex justify-content-between">
                  <span class="text-secondary fw-semibold">Available Slots:</span>
                  <span class="fw-bold text-dark">{{ selectedTrek.slots }}</span>
                </div>
              </div>

              <!-- Status configuration dropdown -->
              <div class="mb-4">
                <label class="form-label fw-bold text-dark text-sm">Status</label>
                <select v-model="selectedTrekStatus" class="form-select custom-select-accent">
                  <option value="Open">Open</option>
                  <option value="Closed">Closed</option>
                  <option value="Completed">Completed</option>
                </select>
              </div>

              <div class="d-flex flex-column gap-2">
                <button class="btn btn-primary-orange w-100 py-2.5" @click="updateSelectedTrekStatus">
                  Update Trek
                </button>
                <button 
                  class="btn btn-outline-success w-100 py-2.5" 
                  :disabled="selectedTrek.status === 'Completed'"
                  @click="markTrekCompleted"
                >
                  Mark as Completed
                </button>
              </div>
            </div>
          </div>

          <!-- Right participants table -->
          <div class="col-12 col-lg-7">
            <div class="dashboard-panel h-100 p-4">
              <div class="d-flex align-items-center justify-content-between mb-4 border-bottom pb-2">
                <h5 class="panel-section-title mb-0">Participants ({{ trekParticipants.length }})</h5>
                <span class="badge bg-light text-dark border">{{ trekParticipants.length }} Registered</span>
              </div>

              <div v-if="trekParticipants.length === 0" class="text-center py-5 text-secondary">
                <span class="fs-1 d-block mb-2">👥</span>
                <p class="mb-0">No participants registered for this trek yet.</p>
              </div>
              <div v-else class="table-responsive">
                <table class="table table-custom align-middle">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Booking Date</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(p, index) in trekParticipants" :key="p.id">
                      <td>{{ index + 1 }}</td>
                      <td class="fw-bold text-dark">{{ p.name }}</td>
                      <td>{{ p.email }}</td>
                      <td>{{ p.bookingDate }}</td>
                      <td>
                        <span class="badge" :class="p.status === 'Confirmed' || p.status === 'Booked' ? 'bg-success' : p.status === 'Pending' ? 'bg-warning text-dark' : 'bg-secondary'">
                          {{ p.status }}
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TAB: Profile -->
      <div v-else-if="currentTab === 'profile'" class="tab-content animate-fade-in">
        <div class="d-flex align-items-center justify-content-between mb-4">
          <h4 class="page-title mb-0">My Profile</h4>
        </div>

        <div class="dashboard-panel">
          <h5 class="panel-section-title mb-4">Account Information</h5>

          <!-- Feedback alerts -->
          <div v-if="profileError" class="alert alert-danger-custom mb-4">
            <i class="bi bi-exclamation-circle-fill me-2"></i> {{ profileError }}
          </div>
          <div v-if="profileSuccess" class="alert alert-success-custom mb-4">
            <i class="bi bi-check-circle-fill me-2"></i> {{ profileSuccess }}
          </div>

          <form @submit.prevent="saveProfile">
            <div class="row g-4">
              <!-- Username -->
              <div class="col-12 col-md-6">
                <label class="form-label text-sm fw-semibold">Username</label>
                <input 
                  v-model="profileForm.username" 
                  type="text" 
                  class="form-control custom-input" 
                  required 
                />
              </div>

              <!-- Email -->
              <div class="col-12 col-md-6">
                <label class="form-label text-sm fw-semibold">Email Address</label>
                <input 
                  v-model="profileForm.email" 
                  type="email" 
                  class="form-control custom-input" 
                  required 
                />
              </div>

              <!-- Phone -->
              <div class="col-12 col-md-6">
                <label class="form-label text-sm fw-semibold">Phone Number</label>
                <input 
                  v-model="profileForm.phone" 
                  type="tel" 
                  class="form-control custom-input" 
                  required 
                />
              </div>

              <!-- Password -->
              <div class="col-12 col-md-6">
                <label class="form-label text-sm fw-semibold">New Password (leave blank to keep current)</label>
                <input 
                  v-model="profileForm.password" 
                  type="password" 
                  placeholder="••••••••" 
                  class="form-control custom-input" 
                />
              </div>
            </div>

            <!-- Submit Button -->
            <div class="d-flex align-items-center justify-content-end gap-3 mt-5">
              <button type="submit" class="btn btn-primary-orange py-2 px-4" :disabled="isSavingProfile">
                <span v-if="isSavingProfile" class="spinner-border spinner-border-sm me-2"></span>
                Save Changes
              </button>
            </div>
          </form>
        </div>
      </div>

      <!-- Fallback Tabs -->
      <div v-else class="dashboard-panel py-5 text-center text-muted animate-fade-in">
        <i class="bi bi-clock-history fs-1 mb-3 d-block text-orange"></i>
        <h5>{{ currentTab.charAt(0).toUpperCase() + currentTab.slice(1) }} Section</h5>
        <p class="text-sm mb-0">This section is currently ready for backend API scheduling logs integration.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/api.js'

const router = useRouter()
const currentTab = ref('dashboard')
const username = ref('Vikram Singh')

const stats = ref({
  assigned_treks: 0,
  total_participants: 0,
  ongoing_treks: 0
})

const assignedTreks = ref([])
const selectedTrek = ref(null)
const selectedTrekStatus = ref('Open')
const trekParticipants = ref([])

// Profile Settings State
const profileForm = ref({
  username: '',
  email: '',
  phone: '',
  password: ''
})
const isSavingProfile = ref(false)
const profileError = ref('')
const profileSuccess = ref('')

const fetchStats = async () => {
  try {
    const response = await api.get('/staff/stats')
    if (response.data && response.data.success) {
      stats.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching staff stats:', error)
  }
}

const fetchAssignedTreks = async () => {
  try {
    const response = await api.get('/staff/treks')
    if (response.data && response.data.success) {
      assignedTreks.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching assigned treks:', error)
  }
}

const handleTrekAction = async (trek) => {
  selectedTrek.value = trek
  selectedTrekStatus.value = trek.status
  currentTab.value = 'manage_trek'
  trekParticipants.value = []
  
  try {
    const response = await api.get(`/staff/treks/${trek.id}/participants`)
    if (response.data && response.data.success) {
      trekParticipants.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching trek participants:', error)
  }
}

const updateSelectedTrekStatus = async () => {
  if (!selectedTrek.value) return
  
  try {
    const response = await api.put(`/staff/treks/${selectedTrek.value.id}/status`, {
      status: selectedTrekStatus.value
    })
    if (response.data && response.data.success) {
      alert('Trek status updated successfully! 🎉')
      await fetchStats()
      await fetchAssignedTreks()
      
      // Update selected status properties locally
      selectedTrek.value.status = selectedTrekStatus.value
    }
  } catch (error) {
    alert(error.response?.data?.message || 'Failed to update trek status')
  }
}

const markTrekCompleted = async () => {
  selectedTrekStatus.value = 'Completed'
  await updateSelectedTrekStatus()
}

const fetchProfile = async () => {
  try {
    const response = await api.get('/profile')
    if (response.data && response.data.success) {
      const data = response.data.data
      profileForm.value.username = data.username
      profileForm.value.email = data.email
      profileForm.value.phone = data.phone || ''
      profileForm.value.password = ''
      username.value = data.username
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

const saveProfile = async () => {
  profileError.value = ''
  profileSuccess.value = ''
  isSavingProfile.value = true
  try {
    const payload = {
      username: profileForm.value.username,
      email: profileForm.value.email,
      phone: profileForm.value.phone
    }
    if (profileForm.value.password) {
      payload.password = profileForm.value.password
    }
    const response = await api.put('/profile', payload)
    if (response.data && response.data.success) {
      profileSuccess.value = 'Profile updated successfully! 🎉'
      setTimeout(() => {
        profileSuccess.value = ''
      }, 3000)
      username.value = profileForm.value.username
      localStorage.setItem('user', JSON.stringify({
        username: profileForm.value.username,
        email: profileForm.value.email,
        role: 'staff'
      }))
      profileForm.value.password = ''
    }
  } catch (error) {
    profileError.value = error.response?.data?.message || 'Failed to update profile'
  } finally {
    isSavingProfile.value = false
  }
}

watch(currentTab, (newTab) => {
  if (newTab === 'profile') {
    fetchProfile()
  }
})

onMounted(async () => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const u = JSON.parse(userStr)
      username.value = u.username || 'Vikram'
    } catch (e) {
      // ignore
    }
  }
  
  await fetchStats()
  await fetchAssignedTreks()
})

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
  router.push('/')
}
</script>

<style scoped>
.dashboard-wrapper {
  --color-bg: #fafaf9;
  --color-card: #ffffff;
  --color-border: #eaeaea;
  --color-text-primary: #1f2937;
  --color-text-secondary: #6b7280;
  --color-accent: #ff6b35;
  --color-accent-light: #fff0eb;
  --font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  
  display: flex;
  min-height: 100vh;
  background-color: var(--color-bg);
  color: var(--color-text-primary);
  font-family: var(--font-family);
}

/* Sidebar Styling */
.sidebar {
  width: 250px;
  background-color: #ffffff;
  border-right: 1px solid #eaeaea;
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  padding: 1.75rem 1.25rem;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-left: 0.5rem;
}

.logo-text {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.03em;
}

.orange-text {
  color: #ff6b35;
}

.logo-badge {
  font-size: 0.65rem;
  font-weight: 700;
  background-color: #fff0eb;
  color: #ff6b35;
  padding: 0.15rem 0.4rem;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  flex-grow: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.75rem 1rem;
  color: #6b7280;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.925rem;
  border-radius: 10px;
  transition: all 0.2s ease-in-out;
}

.nav-item:hover {
  background-color: #fafaf9;
  color: #111827;
}

.nav-item.active {
  background-color: #fff0eb;
  color: #ff6b35;
  font-weight: 600;
}

.nav-icon {
  font-size: 1.15rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.sidebar-footer {
  margin-top: auto;
  border-top: 1px solid #eaeaea;
  padding-top: 1.5rem;
}

.logout-btn {
  color: #ef4444;
}

.logout-btn:hover {
  background-color: #fef2f2;
  color: #dc2626;
}

/* Main Content Area */
.main-content {
  margin-left: 250px;
  flex-grow: 1;
  padding: 2rem 3rem 4rem 3rem;
  max-width: calc(100vw - 250px);
}

.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  height: 50px;
}

.top-bar-actions {
  display: flex;
  align-items: center;
}

.profile-trigger {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.4rem 0.85rem;
  border-radius: 12px;
  border: 1px solid #eaeaea;
  background-color: #ffffff;
}

.avatar-placeholder {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background-color: #ff6b35;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.9rem;
}

.username {
  font-weight: 600;
  font-size: 0.875rem;
  color: #1f2937;
}

.page-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
}

/* Stats Cards */
.stat-card {
  background: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 1.5rem;
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

.stat-card.blue-card::before { background-color: #3b82f6; }
.stat-card.green-card::before { background-color: #22c55e; }
.stat-card.orange-card::before { background-color: #ff6b35; }

.stat-title {
  font-size: 0.825rem;
  font-weight: 600;
  letter-spacing: 0.03em;
}

.stat-value {
  font-size: 2.25rem;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.stat-value.text-blue { color: #3b82f6; }
.stat-value.text-green { color: #22c55e; }
.stat-value.text-orange { color: #ff6b35; }

.stat-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
}

.blue-bg { background-color: #eff6ff; color: #3b82f6; }
.green-bg { background-color: #f0fdf4; color: #166534; }
.orange-bg { background-color: #fff0eb; color: #ff6b35; }

/* Dashboard Panel */
.dashboard-panel {
  background: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 14px;
  padding: 1.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.015);
}

.panel-section-title {
  font-size: 1rem;
  font-weight: 700;
  color: #111827;
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

.status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.2rem 0.65rem;
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: 6px;
}

.status-pill.open {
  background-color: #f0fdf4;
  color: #166534;
}

.status-pill.closed {
  background-color: #f3f4f6;
  color: #4b5563;
}

/* Action Buttons styled like screenshot */
.btn-manage-action {
  background-color: #ffffff;
  color: #ff6b35;
  border: 1.5px solid #ff6b35;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.3rem 1rem;
  border-radius: 6px;
  transition: all 0.2s;
}

.btn-manage-action:hover {
  background-color: #ff6b35;
  color: #ffffff;
}

.btn-view-action {
  background-color: #ffffff;
  color: #ff6b35;
  border: 1.5px solid #ff6b35;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.3rem 1.25rem;
  border-radius: 6px;
  transition: all 0.2s;
  opacity: 0.75;
}

.btn-view-action:hover {
  background-color: #ff6b35;
  color: #ffffff;
  opacity: 1;
}

/* Transitions */
.animate-fade-in {
  animation: fadeIn 0.4s ease-out forwards;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}

.text-sm {
  font-size: 0.875rem;
}
.text-xs {
  font-size: 0.75rem;
}

/* Custom Staff Manage Styles */
.btn-primary-orange {
  background-color: var(--color-accent);
  color: white;
  border: none;
  font-weight: 600;
  border-radius: 8px;
  transition: opacity 0.2s;
}

.btn-primary-orange:hover {
  opacity: 0.9;
  color: white;
}

.btn-outline-success {
  background-color: transparent;
  border: 1.5px solid #10B981;
  color: #10B981;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.2s;
}

.btn-outline-success:hover:not(:disabled) {
  background-color: #10B981;
  color: white;
}

.custom-select-accent {
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 0.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.text-orange {
  color: var(--color-accent);
}

.custom-input {
  border: 1px solid #eaeaea;
  border-radius: 10px;
  font-size: 0.9rem;
  padding: 0.65rem 0.85rem;
  background-color: #fafaf9;
  outline: none;
  transition: all 0.2s;
  width: 100%;
}

.custom-input:focus {
  border-color: #ff6b35;
  background-color: #ffffff;
  box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.15);
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

.alert-success-custom {
  background-color: #f0fdf4;
  border: 1px solid #86efac;
  color: #166534;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
}
</style>
