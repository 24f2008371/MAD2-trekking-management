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
          :stats="stats"
          :dashboard-filtered-treks="dashboardFilteredTreks"
          :difficulty-filter="difficultyFilter"
          :location-filter="locationFilter"
          @update:difficultyFilter="difficultyFilter = $event"
          @update:locationFilter="locationFilter = $event"
          @view-details="viewTrekDetails"
          @change-tab="selectTab"
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
          @update:searchQuery="searchQuery = $event"
          @update:difficultyFilter="difficultyFilter = $event"
          @update:locationFilter="locationFilter = $event"
          @update:currentPage="currentPage = $event"
          @reset-filters="resetFilters"
          @view-details="viewTrekDetails"
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

// Active Tab
const activeTab = ref('dashboard')
const router = useRouter()

const myBookingsList = ref([
  {
    trekName: 'Kedarkantha Trek',
    bookingDate: '10 May 2026',
    trekDates: '15 May - 20 May 2026',
    status: 'Booked'
  },
  {
    trekName: 'Valley of Flowers',
    bookingDate: '12 June 2026',
    trekDates: '05 July - 10 July 2026',
    status: 'Completed'
  }
])

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
  if (activeTab.value === 'dashboard') return `Good Morning, ${profileName.value || 'Ridhi'} 👋`
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
  { id: 'dashboard', name: 'Dashboard', icon: '🏠' },
  { id: 'explore', name: 'Browse Treks', icon: '🥾' },
  { id: 'bookings', name: 'My Bookings', icon: '📅' },
  { id: 'history', name: 'History', icon: '🧾' },
  { id: 'profile', name: 'Profile', icon: '👤' },
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
const treksList = [
  {
    name: 'Everest Base Camp',
    location: 'Nepal',
    difficulty: 'Hard',
    duration: '12 Days',
    slots: 8,
    price: '₹48,000',
    image: 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=600&q=80'
  },
  {
    name: 'Roopkund Trek',
    location: 'Uttarakhand',
    difficulty: 'Moderate',
    duration: '7 Days',
    slots: 7,
    price: '₹12,500',
    image: 'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=600&q=80'
  },
  {
    name: 'Hampta Pass',
    location: 'Himachal',
    difficulty: 'Moderate',
    duration: '5 Days',
    slots: 0,
    price: '₹9,800',
    image: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=80'
  },
  {
    name: 'Valley of Flowers',
    location: 'Uttarakhand',
    difficulty: 'Easy',
    duration: '6 Days',
    slots: 15,
    price: '₹14,500',
    image: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=600&q=80'
  },
  {
    name: 'Goechala Trek',
    location: 'Sikkim',
    difficulty: 'Hard',
    duration: '11 Days',
    slots: 4,
    price: '₹22,000',
    image: 'https://images.unsplash.com/photo-1486915309851-b0cc1f8a0084?w=600&q=80'
  },
  {
    name: 'Kedarkantha Trek',
    location: 'Uttarakhand',
    difficulty: 'Moderate',
    duration: '6 Days',
    slots: 10,
    price: '₹9,500',
    image: 'https://images.unsplash.com/photo-1501555088652-021faa106b9b?w=600&q=80'
  }
]

// Filtered treks specifically for the dashboard (first 3 matching items)
const dashboardFilteredTreks = computed(() => {
  return treksList.filter(trek => {
    const matchesDiff = difficultyFilter.value === 'All' || trek.difficulty === difficultyFilter.value
    const matchesLoc = locationFilter.value === 'All' || trek.location === locationFilter.value
    return matchesDiff && matchesLoc
  }).slice(0, 3)
})

// Filtering logic
const filteredTreks = computed(() => {
  return treksList.filter(trek => {
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

// Watch tab change to fetch profile
watch(activeTab, (newTab) => {
  if (newTab === 'profile') {
    fetchProfile()
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
})

const viewTrekDetails = (trekName) => {
  alert(`Viewing details for: ${trekName}`)
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
</style>
