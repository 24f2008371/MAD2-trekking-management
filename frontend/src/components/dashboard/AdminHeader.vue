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
      <button class="notification-btn" aria-label="Notifications">
        <i class="bi bi-bell"></i>
        <span class="notification-badge"></span>
      </button>
      
      <div class="profile-dropdown" @click="toggleDropdown" v-click-outside="closeDropdown">
        <div class="profile-trigger">
          <div class="avatar-placeholder">A</div>
          <span class="username">{{ profileName || 'Admin' }}</span>
          <i class="bi bi-chevron-down dropdown-arrow" :class="{ rotated: dropdownOpen }"></i>
        </div>
        <transition name="slide-fade">
          <div v-if="dropdownOpen" class="dropdown-menu-custom">
            <router-link to="/admin/settings"><i class="bi bi-gear"></i> Settings</router-link>
            <hr class="dropdown-divider" />
            <a href="#" @click.prevent="$emit('logout')" class="text-danger"><i class="bi bi-box-arrow-right"></i> Logout</a>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

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
const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}
const closeDropdown = () => {
  dropdownOpen.value = false
}

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
}

.notification-btn:hover {
  background-color: #ffffff;
  border-color: #d1d1d1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.notification-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 8px;
  height: 8px;
  background-color: #ff6b35;
  border-radius: 50%;
  border: 1.5px solid #ffffff;
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
