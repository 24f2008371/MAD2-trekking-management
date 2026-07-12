<template>
  <header class="top-bar">
    <div class="welcome-message">
      <h1>{{ pageTitle }}</h1>
      <p class="subtitle">{{ pageSubtitle }}</p>
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
              <span class="notif-title">Notifications</span>
              <span v-if="unreadCount > 0" class="notif-count">{{ unreadCount }} new</span>
            </div>
            <div class="notif-list" v-if="notifications.length > 0">
              <div v-for="notif in notifications" :key="notif.id" class="notif-item" :class="{ unread: !notif.read }">
                <i class="bi" :class="notif.icon"></i>
                <div class="notif-content">
                  <p class="notif-text">{{ notif.message }}</p>
                  <span class="notif-time">{{ notif.time }}</span>
                </div>
              </div>
            </div>
            <div v-else class="notif-empty">
              <i class="bi bi-bell-slash"></i>
              <p>No notifications yet</p>
            </div>
          </div>
        </transition>
      </div>
      
      <div class="profile-dropdown" @click="toggleDropdown" v-click-outside="closeDropdown">
        <div class="profile-trigger">
          <img :src="avatarUrl" :alt="profileName || 'Ridhi'" class="avatar" />
          <span class="username">{{ profileName || 'Ridhi' }}</span>
          <i class="bi bi-chevron-down dropdown-arrow" :class="{ rotated: dropdownOpen }"></i>
        </div>
        <transition name="slide-fade">
          <div v-if="dropdownOpen" class="dropdown-menu-custom">
            <a href="#" @click.prevent="$emit('select-tab', 'profile')"><i class="bi bi-person"></i> My Profile</a>
            <hr class="dropdown-divider" />
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
  avatarUrl: {
    type: String,
    required: true
  },
  profileName: {
    type: String,
    required: true
  }
})

defineEmits(['select-tab', 'logout'])

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

const fetchNotifications = async () => {
  try {
    const response = await api.get('/bookings')
    if (response.data && response.data.success) {
      const bookings = response.data.data
      notifications.value = bookings.slice(0, 5).map((b, i) => ({
        id: i,
        message: `Booking ${b.id} for "${b.trekName}" is ${b.status}`,
        time: b.bookingDate || 'Recently',
        icon: b.status === 'Confirmed' ? 'bi-check-circle-fill text-success' : b.status === 'Cancelled' ? 'bi-x-circle-fill text-danger' : 'bi-clock-fill text-warning',
        read: b.status !== 'Pending'
      }))
    }
  } catch (error) {
    console.error('Error fetching notifications:', error)
  }
}

onMounted(() => {
  fetchNotifications()
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
  margin-bottom: 3.5rem;
}

.welcome-message h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.25rem;
  letter-spacing: -0.02em;
}

.welcome-message .subtitle {
  color: var(--color-text-secondary);
  font-size: 0.95rem;
  margin: 0;
}

.top-bar-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.notification-wrapper {
  position: relative;
}

.notification-btn {
  background: transparent;
  border: 1px solid var(--color-border);
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-primary);
  font-size: 1.15rem;
  position: relative;
  transition: all 0.2s ease;
  cursor: pointer;
}

.notification-btn:hover {
  background-color: #FFFFFF;
  border-color: #D1D1D1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.notification-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background-color: #FF6B35;
  border-radius: 20px;
  border: 2px solid #fff;
  font-size: 0.6rem;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-panel {
  position: absolute;
  right: 0;
  top: calc(100% + 10px);
  width: 320px;
  background-color: #fff;
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
  color: #FF6B35;
  background: #FFF3ED;
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
  background: #FFFBF7;
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
  border: 1px solid var(--color-border);
  background-color: var(--color-card);
  transition: all 0.2s ease;
}

.profile-trigger:hover {
  border-color: #D1D1D1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  object-fit: cover;
}

.username {
  font-weight: 600;
  font-size: 0.925rem;
  color: var(--color-text-primary);
}

.dropdown-arrow {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
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
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
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
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.15s ease;
}

.dropdown-menu-custom a:hover {
  background-color: var(--color-bg);
  color: var(--color-text-primary);
}

.dropdown-divider {
  margin: 0.4rem 0;
  border-top: 1px solid var(--color-border);
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
