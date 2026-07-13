<template>
  <header class="top-bar">
    <div class="d-flex align-items-center gap-3">
      <!-- Toggle button for Sidebar -->
      <button class="toggle-sidebar-btn" @click="$emit('toggle-sidebar')" aria-label="Toggle Sidebar">
        <i class="bi" :class="isSidebarCollapsed ? 'bi-text-indent-left' : 'bi-text-indent-right'"></i>
      </button>
      <div class="welcome-message">
        <h1>{{ pageTitle }}</h1>
        <p class="subtitle">{{ pageSubtitle }}</p>
      </div>
    </div>
    <div class="top-bar-actions">
      <div class="notification-wrapper" @click="toggleNotifications" v-click-outside="closeNotifications">
        <button class="notification-btn" aria-label="Notifications">
          <i class="bi bi-bell"></i>
          <span v-if="unreadCount > 0" class="notification-badge">{{ unreadCount }}</span>
        </button>
        <transition name="slide-fade">
          <div v-if="notificationsOpen" class="notification-panel">
            <div class="notif-header">
              <span class="notif-title">Admin Alerts</span>
              <span v-if="unreadCount > 0" class="notif-count">{{ unreadCount }} pending</span>
            </div>
            <div class="notif-list" v-if="notifications.length > 0">
              <div v-for="notif in notifications" :key="notif.id" class="notif-item" :class="{ unread: !notif.read }">
                <i class="bi bi-clock-fill text-warning"></i>
                <div class="notif-content">
                  <p class="notif-text"><strong>{{ notif.username }}</strong> requested booking for <strong>{{ notif.trek }}</strong></p>
                  <span class="notif-time">{{ notif.time }}</span>
                </div>
              </div>
            </div>
            <div v-else class="notif-empty">
              <i class="bi bi-check2-all text-success"></i>
              <p>All bookings cleared!</p>
            </div>
          </div>
        </transition>
      </div>
      
      <div class="profile-dropdown" @click="toggleDropdown" v-click-outside="closeDropdown">
        <div class="profile-trigger">
          <div class="avatar-placeholder">A</div>
          <span class="username">{{ profileName || 'Admin' }}</span>
          <i class="bi bi-chevron-down dropdown-arrow" :class="{ rotated: dropdownOpen }"></i>
        </div>
        <transition name="slide-fade">
          <div v-if="dropdownOpen" class="dropdown-menu-custom">
            <a href="#" @click.prevent="$emit('logout')" class="text-danger"><i class="bi bi-box-arrow-right"></i> Logout</a>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../../api/api.js'

defineProps({
  pageTitle: {
    type: String,
    required: true
  },
  pageSubtitle: {
    type: String,
    required: true
  },
  profileName: {
    type: String,
    default: 'Admin'
  },
  isSidebarCollapsed: {
    type: Boolean,
    default: false
  }
})

defineEmits(['logout', 'toggle-sidebar'])

const dropdownOpen = ref(false)
const notificationsOpen = ref(false)
const notifications = ref([])

const unreadCount = computed(() => notifications.value.filter(n => !n.read).length)

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
  notificationsOpen.value = false
}
const closeDropdown = () => {
  dropdownOpen.value = false
}

const toggleNotifications = () => {
  notificationsOpen.value = !notificationsOpen.value
  dropdownOpen.value = false
  if (notificationsOpen.value) {
    notifications.value.forEach(n => n.read = true)
  }
}
const closeNotifications = () => {
  notificationsOpen.value = false
}

const fetchAdminNotifications = async () => {
  try {
    const response = await api.get('/admin/bookings')
    if (response.data && response.data.success) {
      const bookings = response.data.data
      // Filter for pending bookings that require admin action
      const pendingBookings = bookings.filter(b => b.status === 'Pending')
      notifications.value = pendingBookings.slice(0, 5).map((b, i) => ({
        id: b.id || i,
        username: b.user || 'User',
        trek: b.trek || 'Trek',
        time: b.date || 'Today',
        read: false
      }))
    }
  } catch (error) {
    console.error('Error fetching admin notifications:', error)
  }
}

onMounted(() => {
  fetchAdminNotifications()
})

// Custom directive for clicking outside dropdown
const vClickOutside = {
  mounted(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.removeEventListener('click', el.clickOutsideEvent)
  }
}
</script>

<style scoped>
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
}

.toggle-sidebar-btn {
  background: transparent;
  border: 1px solid #eaeaea;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1f2937;
  font-size: 1.25rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.toggle-sidebar-btn:hover {
  background-color: #ffffff;
  border-color: #d1d1d1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.welcome-message h1 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.welcome-message .subtitle {
  color: #6b7280;
  font-size: 0.875rem;
  margin: 0;
}

.top-bar-actions {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.notification-wrapper {
  position: relative;
}

.notification-btn {
  background: transparent;
  border: 1px solid #eaeaea;
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #1f2937;
  font-size: 1.15rem;
  position: relative;
  transition: all 0.2s ease;
  cursor: pointer;
}

.notification-btn:hover {
  background-color: #ffffff;
  border-color: #d1d1d1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.notification-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background-color: #ff6b35;
  border-radius: 20px;
  border: 2px solid #ffffff;
  font-size: 0.6rem;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-panel {
  position: absolute;
  right: 0;
  top: calc(100% + 10px);
  width: 320px;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.1);
  z-index: 200;
  overflow: hidden;
}

.notif-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 16px;
  border-bottom: 1px solid #f1f5f9;
}

.notif-title {
  font-weight: 700;
  font-size: 0.9rem;
  color: #111827;
}

.notif-count {
  font-size: 0.7rem;
  font-weight: 600;
  color: #ffffff;
  background: #ff6b35;
  padding: 2px 8px;
  border-radius: 20px;
}

.notif-list {
  max-height: 280px;
  overflow-y: auto;
}

.notif-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  border-bottom: 1px solid #f9fafb;
  transition: background 0.15s ease;
}

.notif-item:last-child {
  border-bottom: none;
}

.notif-item.unread {
  background: #fffbf7;
}

.notif-item:hover {
  background: #f8fafc;
}

.notif-item > i {
  font-size: 1.1rem;
  margin-top: 2px;
  flex-shrink: 0;
}

.notif-content {
  flex: 1;
  min-width: 0;
}

.notif-text {
  font-size: 0.8rem;
  color: #334155;
  margin: 0 0 3px 0;
  line-height: 1.35;
}

.notif-time {
  font-size: 0.7rem;
  color: #94a3b8;
}

.notif-empty {
  padding: 30px 16px;
  text-align: center;
  color: #94a3b8;
}

.notif-empty i {
  font-size: 1.8rem;
  display: block;
  margin-bottom: 8px;
}

.notif-empty p {
  font-size: 0.85rem;
  margin: 0;
}

.profile-dropdown {
  position: relative;
  cursor: pointer;
}

.profile-trigger {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.35rem 0.75rem 0.35rem 0.35rem;
  border-radius: 12px;
  border: 1px solid #eaeaea;
  background-color: #ffffff;
  transition: all 0.2s ease;
}

.profile-trigger:hover {
  border-color: #d1d1d1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background-color: #ff6b35;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.95rem;
}

.username {
  font-weight: 600;
  font-size: 0.925rem;
  color: #1f2937;
}

.dropdown-arrow {
  font-size: 0.75rem;
  color: #6b7280;
  transition: transform 0.2s ease;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

.dropdown-menu-custom {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  width: 180px;
  background-color: #ffffff;
  border: 1px solid #eaeaea;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
  padding: 0.5rem;
  z-index: 101;
  display: flex;
  flex-direction: column;
}

.dropdown-menu-custom a {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.6rem 0.75rem;
  color: #6b7280;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.15s ease;
}

.dropdown-menu-custom a:hover {
  background-color: #fafaf9;
  color: #111827;
}

.dropdown-divider {
  margin: 0.4rem 0;
  border-top: 1px solid #eaeaea;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.15s ease-out;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-4px);
  opacity: 0;
}
</style>
