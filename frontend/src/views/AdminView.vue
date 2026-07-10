<template>
  <div class="dashboard-wrapper">
    <!-- Collapsible Sidebar -->
    <AdminSidebar 
      :is-collapsed="isSidebarCollapsed"
      @logout="handleLogout" 
    />

    <!-- Main Content Area -->
    <main class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- Top Bar Header -->
      <AdminHeader 
        :page-title="pageTitle" 
        :page-subtitle="pageSubtitle" 
        :profile-name="profileName" 
        :is-sidebar-collapsed="isSidebarCollapsed"
        @toggle-sidebar="toggleSidebar"
        @logout="handleLogout" 
      />

      <!-- Subview Transition Container -->
      <router-view v-slot="{ Component }">
        <transition name="tab-fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AdminSidebar from '../components/dashboard/AdminSidebar.vue'
import AdminHeader from '../components/dashboard/AdminHeader.vue'

const router = useRouter()
const route = useRoute()

const isSidebarCollapsed = ref(false)
const profileName = ref('Admin')

const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value
}

// Compute page titles dynamically from current route name
const pageTitle = computed(() => {
  switch (route.name) {
    case 'AdminDashboard': return 'Dashboard Overview'
    case 'AdminTreks': return 'Treks Management'
    case 'AdminStaff': return 'Trekking Staff'
    case 'AdminUsers': return 'Registered Trekkers'
    case 'AdminBookings': return 'Bookings Registry'
    case 'AdminSearch': return 'Search Portal'
    case 'AdminReports': return 'Analytics & Reports'
    case 'AdminSettings': return 'Portal Settings'
    default: return 'Admin Console'
  }
})

const pageSubtitle = computed(() => {
  switch (route.name) {
    case 'AdminDashboard': return 'Welcome back! Here is a summary of the trekking operations.'
    case 'AdminTreks': return 'Manage expedition destinations, difficulty levels, and pricing.'
    case 'AdminStaff': return 'Coordinate local guides, coordinators, and medical crew.'
    case 'AdminUsers': return 'Track user accounts, registration dates, and status logs.'
    case 'AdminBookings': return 'Approve, review, or cancel active reservation requests.'
    case 'AdminSearch': return 'Perform global queries across all dataset tables.'
    case 'AdminReports': return 'Track performance indexes, charts, and revenue statistics.'
    case 'AdminSettings': return 'Manage system constants, support email, and restrictions.'
    default: return 'Manage TrekMate administrative tasks.'
  }
})

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const u = JSON.parse(userStr)
      profileName.value = u.username || 'Admin'
    } catch (e) {
      // ignore
    }
  }
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

.main-content {
  margin-left: 260px;
  flex-grow: 1;
  padding: 2rem 3rem 4rem 3rem;
  max-width: calc(100vw - 260px);
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1), max-width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.main-content.sidebar-collapsed {
  margin-left: 78px;
  max-width: calc(100vw - 78px);
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
  .main-content, .main-content.sidebar-collapsed {
    margin-left: 0;
    max-width: 100vw;
    padding: 1.5rem 1.5rem 3rem 1.5rem;
  }
}
</style>
