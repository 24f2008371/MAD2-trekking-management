<template>
  <div class="dashboard-wrapper">
    <!-- Slim Sidebar -->
    <UserSidebar 
      :active-tab="activeTab" 
      :nav-items="navItems" 
      @select-tab="selectTab" 
      @logout="handleLogout" 
    />

    <!-- Main Content Area -->
    <main class="main-content">
      <!-- Top Bar -->
      <UserHeader 
        :page-title="pageTitle" 
        :page-subtitle="pageSubtitle" 
        :avatar-url="avatarUrl" 
        :profile-name="profileName" 
        @select-tab="selectTab" 
        @logout="handleLogout" 
      />

      <transition name="tab-fade" mode="out-in">
        <!-- Dashboard Tab Container -->
        <DashboardTab
          v-if="activeTab === 'dashboard'"
          key="dashboard"
          :dashboard-filtered-treks="dashboardFilteredTreks"
          :difficulty-filter="difficultyFilter"
          :location-filter="locationFilter"
          :my-bookings-list="myBookingsList"
          @update:difficultyFilter="difficultyFilter = $event"
          @update:locationFilter="locationFilter = $event"
          @view-details="viewTrekDetails"
          @change-tab="selectTab"
          @book-trek="bookTrek"
        />

        <!-- Browse Treks Tab Container -->
        <ExploreTab
          v-else-if="activeTab === 'explore'"
          key="explore"
          :search-query="searchQuery"
          :difficulty-filter="difficultyFilter"
          :location-filter="locationFilter"
          :current-page="currentPage"
          :paginated-treks="paginatedTreks"
          :total-pages="totalPages"
          :filtered-treks="filteredTreks"
          :my-bookings-list="myBookingsList"
          @update:searchQuery="searchQuery = $event"
          @update:difficultyFilter="difficultyFilter = $event"
          @update:locationFilter="locationFilter = $event"
          @update:currentPage="currentPage = $event"
          @reset-filters="resetFilters"
          @view-details="viewTrekDetails"
          @book-trek="bookTrek"
        />

        <!-- Profile Tab Container -->
        <ProfileTab
          v-else-if="activeTab === 'profile'"
          key="profile"
          :profile-name="profileName"
          :profile-email="profileEmail"
          :profile-phone="profilePhone"
          :profile-password="profilePassword"
          :is-saving-profile="isSavingProfile"
          :profile-error="profileError"
          :profile-success="profileSuccess"
          :custom-avatar-input="customAvatarInput"
          :avatar-url="avatarUrl"
          :avatar-presets="avatarPresets"
          @update:profileName="profileName = $event"
          @update:profileEmail="profileEmail = $event"
          @update:profilePhone="profilePhone = $event"
          @update:profilePassword="profilePassword = $event"
          @update:customAvatarInput="customAvatarInput = $event"
          @save-profile="saveProfile"
          @save-avatar="saveAvatar"
          @cancel="activeTab = 'dashboard'"
        />

        <!-- My Bookings Tab Container -->
        <BookingsTab
          v-else-if="activeTab === 'bookings'"
          key="bookings"
          :my-bookings-list="myBookingsList"
          @view-details="viewTrekDetails"
        />

        <!-- Trekking History Tab Container -->
        <HistoryTab
          v-else-if="activeTab === 'history'"
          key="history"
          :history-list="historyList"
        />

        <!-- Other Tabs Fallback -->
        <div v-else key="fallback" class="dashboard-container py-5">
          <div class="empty-state-container">
            <span class="empty-state-icon">⚙️</span>
            <h3>{{ getTabName(activeTab) }}</h3>
            <p>This section is currently under development to integrate clean SaaS features.</p>
            <button class="btn btn-primary-accent mt-3" @click="activeTab = 'dashboard'">Return to Dashboard</button>
          </div>
        </div>
      </transition>
    </main>

    <!-- Premium Trek Details Modal -->
    <div v-if="selectedTrek" class="premium-details-overlay" @click="selectedTrek = null">
      <div class="premium-details-card" @click.stop>
        <button class="close-btn" @click="selectedTrek = null">
          <i class="bi bi-x-lg"></i>
        </button>

        <div class="details-image-wrapper">
          <img :src="selectedTrek.image" :alt="selectedTrek.name" class="details-image" />
          <span class="difficulty-badge" :class="selectedTrek.difficulty.toLowerCase()">
            {{ selectedTrek.difficulty }}
          </span>
        </div>

        <div class="details-body p-4 text-start">
          <h3 class="font-heading text-navy mb-2" style="font-weight: 700;">{{ selectedTrek.name }}</h3>
          
          <div class="d-flex align-items-center gap-3 text-secondary text-sm mb-4">
            <span><i class="bi bi-geo-alt-fill text-orange"></i> {{ selectedTrek.location }}</span>
            <span>•</span>
            <span><i class="bi bi-clock-fill text-orange"></i> {{ selectedTrek.duration }}</span>
          </div>

          <div class="row g-2 mb-4">
            <div class="col-6">
              <div class="info-card p-2 rounded-3 bg-light">
                <span class="d-block text-xs text-muted mb-0">Departure Date</span>
                <span class="fw-semibold text-dark text-sm">{{ selectedTrek.start_date || 'TBD' }}</span>
              </div>
            </div>
            <div class="col-6">
              <div class="info-card p-2 rounded-3 bg-light">
                <span class="d-block text-xs text-muted mb-0">Return Date</span>
                <span class="fw-semibold text-dark text-sm">{{ selectedTrek.end_date || 'TBD' }}</span>
              </div>
            </div>
            <div class="col-6">
              <div class="info-card p-2 rounded-3 bg-light">
                <span class="d-block text-xs text-muted mb-0">Available Slots</span>
                <span class="fw-semibold text-sm" :class="selectedTrek.slots > 0 ? 'text-success' : 'text-danger'">
                  {{ selectedTrek.slots }} left
                </span>
              </div>
            </div>
            <div class="col-6">
              <div class="info-card p-2 rounded-3 bg-light">
                <span class="d-block text-xs text-muted mb-0">Price per Person</span>
                <span class="fw-bold text-orange text-sm">{{ selectedTrek.price }}</span>
              </div>
            </div>
          </div>

          <div class="d-flex gap-2">
            <button class="btn btn-secondary-outline w-50 py-2 text-xs" @click="selectedTrek = null">Close</button>
            <button 
              class="btn btn-primary-accent w-50 py-2 text-xs" 
              :disabled="selectedTrek.slots === 0"
              @click="bookTrek(selectedTrek.id); selectedTrek = null"
            >
              {{ selectedTrek.slots > 0 ? 'Book Expedition' : 'Fully Booked' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Premium Payment Modal -->
    <div v-if="payingTrek" class="premium-alert-overlay" @click="payingTrek = null">
      <div class="premium-alert-box" @click.stop style="max-width: 420px;">
        <div class="alert-icon success" style="background-color: #FFF0EB;">
          <span style="color: var(--color-accent); font-size: 2rem;">💳</span>
        </div>
        <h4 class="alert-title">Secure Checkout</h4>
        <p class="alert-text mb-3">You are booking <strong>{{ payingTrek.name }}</strong> for <strong>{{ payingTrek.price }}</strong>.</p>
        
        <div class="p-3 rounded-3 bg-light border mb-4 text-start">
          <div class="d-flex align-items-center justify-content-between mb-2">
            <span class="text-xs text-muted" style="font-weight: 700; text-transform: uppercase;">Payment Method</span>
            <span class="badge bg-success text-xs">Simulated</span>
          </div>
          <div class="d-flex align-items-center gap-2">
            <i class="bi bi-credit-card-2-back text-orange fs-4"></i>
            <span class="text-sm fw-semibold">TrekMate Secure Payment Wallet</span>
          </div>
        </div>

        <div class="d-flex gap-2">
          <button class="btn btn-secondary-outline w-50 py-2 text-xs" @click="payingTrek = null">Cancel</button>
          <button class="btn btn-primary-accent w-50 py-2 text-xs" @click="confirmPaymentAndBook">Pay Now</button>
        </div>
      </div>
    </div>

    <!-- Premium Alert Modal -->
    <div v-if="alertMessage" class="premium-alert-overlay" @click="closeAlert">
      <div class="premium-alert-box" @click.stop>
        <div class="alert-icon" :class="alertType">
          <span v-if="alertType === 'success'">🎉</span>
          <span v-else>⚠️</span>
        </div>
        <h4 class="alert-title">{{ alertType === 'success' ? 'Success' : 'Message' }}</h4>
        <p class="alert-text">{{ alertMessage }}</p>
        <button class="btn btn-primary-accent w-100 mt-2" @click="closeAlert">OK</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/api.js'

// Import dashboard components
import UserSidebar from '../components/dashboard/UserSidebar.vue'
import UserHeader from '../components/dashboard/UserHeader.vue'
import DashboardTab from '../components/dashboard/DashboardTab.vue'
import ExploreTab from '../components/dashboard/ExploreTab.vue'
import ProfileTab from '../components/dashboard/ProfileTab.vue'
import BookingsTab from '../components/dashboard/BookingsTab.vue'
import HistoryTab from '../components/dashboard/HistoryTab.vue'

// Active Tab
const activeTab = ref('dashboard')
const router = useRouter()

const myBookingsList = ref([])
const selectedTrek = ref(null)
const payingTrek = ref(null)

// Alert state
const alertMessage = ref('')
const alertType = ref('success')

const closeAlert = () => {
  alertMessage.value = ''
}


// Profile variables
const profileName = ref('')
const profileEmail = ref('')
const profilePhone = ref('')
const profilePassword = ref('')
const isSavingProfile = ref(false)
const profileError = ref('')
const profileSuccess = ref('')
const customAvatarInput = ref('')

const avatarPresets = [
  '/dog1.png',
  '/dog2.png',
  '/dog3.png',
  '/dog4.png',
  'https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=150',
  'https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=150'
]

const avatarUrl = ref(localStorage.getItem('avatar_url') || avatarPresets[0])

const saveAvatar = (url) => {
  if (!url) return
  avatarUrl.value = url
  localStorage.setItem('avatar_url', url)
  customAvatarInput.value = url
}

// Search & Filter state
const searchQuery = ref('')
const difficultyFilter = ref('All')
const locationFilter = ref('All')
const currentPage = ref(1)

// Reset filters
const resetFilters = () => {
  searchQuery.value = ''
  difficultyFilter.value = 'All'
  locationFilter.value = 'All'
  currentPage.value = 1
}

// Reset page on filter changes
watch([searchQuery, difficultyFilter, locationFilter], () => {
  currentPage.value = 1
})

// Tab navigation wrapper
const selectTab = (tabId) => {
  activeTab.value = tabId
  resetFilters()
}

// Page title and subtitle helpers
const pageTitle = computed(() => {
  if (activeTab.value === 'dashboard') return `Good Morning, ${profileName.value || 'Ridhi'}`
  if (activeTab.value === 'explore') return 'Browse Treks'
  return getTabName(activeTab.value)
})

const pageSubtitle = computed(() => {
  if (activeTab.value === 'dashboard') return 'Ready for your next adventure?'
  if (activeTab.value === 'explore') return 'Find and book the perfect trekking experience.'
  if (activeTab.value === 'profile') return 'Update your personal details and preferences.'
  return 'TrekMate Premium Portal'
})

const getTabName = (tabId) => {
  const item = navItems.find(n => n.id === tabId)
  return item ? item.name : 'TrekMate'
}

// Navigation Items
const navItems = [
  { id: 'dashboard', name: 'Dashboard', icon: '<i class="bi bi-grid"></i>' },
  { id: 'explore', name: 'Browse Treks', icon: '<i class="bi bi-compass"></i>' },
  { id: 'bookings', name: 'My Bookings', icon: '<i class="bi bi-journal-check"></i>' },
  { id: 'history', name: 'History', icon: '<i class="bi bi-clock-history"></i>' },
  { id: 'profile', name: 'Profile', icon: '<i class="bi bi-person"></i>' },
]

// Stats Cards data
const stats = [
  {
    title: 'Upcoming Treks',
    value: '1',
    icon: '🏔',
    trend: '+1 this month',
    trendType: 'positive'
  },
  {
    title: 'Completed Treks',
    value: '12',
    icon: '🥾',
    trend: '84% completion',
    trendType: 'neutral'
  },
  {
    title: 'Total Bookings',
    value: '13',
    icon: '📅',
    trend: 'All time',
    trendType: 'positive'
  },
  {
    title: 'Reward Points',
    value: '2,450',
    icon: '🪙',
    trend: 'Gold Level',
    trendType: 'premium'
  }
]

// Master Treks list
const treksList = ref([])

const fetchTreks = async () => {
  try {
    const response = await api.get('/treks')
    if (response.data && response.data.success) {
      treksList.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching treks:', error)
  }
}

// Fetch user bookings
const fetchBookings = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  
  try {
    const response = await api.get('/bookings', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    if (response.data && response.data.success) {
      myBookingsList.value = response.data.data
    }
  } catch (error) {
    console.error('Error fetching user bookings:', error)
  }
}

// Book a trek
const bookTrek = async (trekId) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alertType.value = 'error'
    alertMessage.value = 'Please log in to book a trek.'
    router.push('/auth/login')
    return
  }
  
  const trek = treksList.value.find(t => t.id === trekId)
  if (trek) {
    payingTrek.value = trek
  }
}

// Confirm checkout and pay
const confirmPaymentAndBook = async () => {
  if (!payingTrek.value) return
  
  const token = localStorage.getItem('access_token')
  const trekId = payingTrek.value.id
  payingTrek.value = null // close payment modal
  
  try {
    const response = await api.post('/bookings', {
      trek_id: trekId
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    if (response.data && response.data.success) {
      alertType.value = 'success'
      alertMessage.value = 'Payment Successful! Booking request sent to admin for approval. 🎉'
      
      // Update stats and lists reactively
      await fetchTreks()
      await fetchBookings()
    }
  } catch (error) {
    alertType.value = 'error'
    if (error.response && error.response.data && error.response.data.message) {
      alertMessage.value = error.response.data.message
    } else {
      alertMessage.value = 'Failed to process payment. Please try again.'
    }
  }
}

// Filtered treks specifically for the dashboard (first 3 matching items)
const dashboardFilteredTreks = computed(() => {
  return treksList.value.filter(trek => {
    const matchesDiff = difficultyFilter.value === 'All' || trek.difficulty === difficultyFilter.value
    const matchesLoc = locationFilter.value === 'All' || trek.location === locationFilter.value
    return matchesDiff && matchesLoc
  }).slice(0, 3)
})

// Compute history list from completed bookings
const historyList = computed(() => {
  return myBookingsList.value.filter(b => b.status === 'Completed')
})

// Filtering logic
const filteredTreks = computed(() => {
  return treksList.value.filter(trek => {
    const matchesSearch = trek.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          trek.location.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesDiff = difficultyFilter.value === 'All' || trek.difficulty === difficultyFilter.value
    const matchesLoc = locationFilter.value === 'All' || trek.location === locationFilter.value
    return matchesSearch && matchesDiff && matchesLoc
  })
})

// Pagination logic
const itemsPerPage = 6
const totalPages = computed(() => Math.ceil(filteredTreks.value.length / itemsPerPage))
const paginatedTreks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filteredTreks.value.slice(start, start + itemsPerPage)
})

// Fetch profile details
const fetchProfile = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return
  
  try {
    const response = await api.get('/profile', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    if (response.data && response.data.data) {
      const u = response.data.data
      profileName.value = u.username
      profileEmail.value = u.email
      profilePhone.value = u.phone
      
      // Update local storage user just in case
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        const uObj = JSON.parse(storedUser)
        uObj.username = u.username
        uObj.email = u.email
        localStorage.setItem('user', JSON.stringify(uObj))
      }
    }
  } catch (error) {
    console.error('Error fetching profile:', error)
  }
}

const saveProfile = async () => {
  profileError.value = ''
  profileSuccess.value = ''
  
  const token = localStorage.getItem('access_token')
  if (!token) {
    profileError.value = 'Not authenticated.'
    return
  }
  
  isSavingProfile.value = true
  try {
    const response = await api.put('/profile', {
      username: profileName.value,
      email: profileEmail.value,
      phone: profilePhone.value,
      password: profilePassword.value || undefined
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    
    if (response.data && response.data.success) {
      profileSuccess.value = response.data.message || 'Profile updated successfully.'
      profilePassword.value = ''
      
      // Update local storage user
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        const uObj = JSON.parse(storedUser)
        uObj.username = profileName.value
        uObj.email = profileEmail.value
        localStorage.setItem('user', JSON.stringify(uObj))
      }
    }
  } catch (error) {
    if (error.response && error.response.data && error.response.data.message) {
      profileError.value = error.response.data.message
    } else {
      profileError.value = 'Failed to update profile.'
    }
  } finally {
    isSavingProfile.value = false
  }
}

// Watch tab change to fetch profile, treks, or bookings
watch(activeTab, (newTab) => {
  if (newTab === 'profile') {
    fetchProfile()
  }
  if (newTab === 'explore' || newTab === 'dashboard') {
    fetchTreks()
    fetchBookings()
  }
  if (newTab === 'bookings') {
    fetchBookings()
  }
})

onMounted(() => {
  const token = localStorage.getItem('access_token')
  const userStr = localStorage.getItem('user')
  if (token && userStr) {
    try {
      const u = JSON.parse(userStr)
      profileName.value = u.username
      profileEmail.value = u.email
    } catch (e) {
      // ignore
    }
  }
  fetchProfile()
  fetchTreks()
  fetchBookings()
})

const viewTrekDetails = (trekName) => {
  const trek = treksList.value.find(t => t.name === trekName)
  if (trek) {
    selectedTrek.value = trek
  }
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user')
  router.push('/')
}
</script>

<style scoped>
/* Color variables tailored to User dashboard requirements */
.dashboard-wrapper {
  --color-bg: #FAFAF8;
  --color-card: #FFFFFF;
  --color-border: #EAEAEA;
  --color-text-primary: #1F2937;
  --color-text-secondary: #6B7280;
  --color-accent: #FF6B35;
  --color-accent-light: #FFF0EB;
  --font-family: 'Poppins', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  
  display: flex;
  min-height: 100vh;
  background-color: var(--color-bg);
  color: var(--color-text-primary);
  font-family: var(--font-family);
}

/* Main Content Area */
.main-content {
  margin-left: 240px;
  flex-grow: 1;
  padding: 2rem 3rem 4rem 3rem;
  max-width: calc(100vw - 240px);
}

/* Tab Switching Transitions */
.tab-fade-enter-active,
.tab-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
}
.tab-fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}
.tab-fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

/* Responsive Overrides */
@media (max-width: 991.98px) {
  .main-content {
    margin-left: 0;
    max-width: 100vw;
    padding: 1.5rem 1.5rem 3rem 1.5rem;
  }
}

/* Fallback Tab Styles */
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

.empty-state-container {
  padding: 3rem 1.5rem;
  background-color: var(--color-card);
  border: 1px dashed var(--color-border);
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-state-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.empty-state-container h3 {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.empty-state-container p {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-bottom: 0;
}

.btn-primary-accent {
  background-color: var(--color-accent);
  color: #FFFFFF;
  border: none;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  transition: opacity 0.2s ease;
}

.btn-primary-accent:hover {
  opacity: 0.9;
  color: #FFFFFF;
}

/* Premium Alert Modal Styles */
.premium-alert-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.premium-alert-box {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  border-radius: 16px;
  width: 90%;
  max-width: 400px;
  padding: 2rem;
  text-align: center;
  animation: slide-up-alert 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

@keyframes slide-up-alert {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.alert-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  margin-left: auto;
  margin-right: auto;
}

.alert-icon.success {
  background-color: #E6FDF4;
}

.alert-icon.error {
  background-color: #FEE2E2;
}

.alert-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary);
}

.alert-text {
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

/* Premium Trek Details Modal Styles */
.premium-details-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9990;
  padding: 1.5rem;
}

.premium-details-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  width: 100%;
  max-width: 480px;
  overflow: hidden;
  position: relative;
  animation: scale-up-details 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

@keyframes scale-up-details {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(15, 23, 42, 0.6);
  border: none;
  color: white;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.close-btn:hover {
  background: rgba(15, 23, 42, 0.8);
}

.details-image-wrapper {
  position: relative;
  height: 200px;
  width: 100%;
}

.details-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.details-image-wrapper .difficulty-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.35rem 0.75rem;
  border-radius: 50px;
  text-transform: uppercase;
}

.difficulty-badge.easy { background-color: #10B981; }
.difficulty-badge.moderate { background-color: #F59E0B; color: #1F2937; }
.difficulty-badge.hard { background-color: #EF4444; }
.difficulty-badge.difficult { background-color: #EF4444; }

.info-card {
  border: 1px solid var(--color-border);
}

.line-height-15 {
  line-height: 1.6;
}
</style>
