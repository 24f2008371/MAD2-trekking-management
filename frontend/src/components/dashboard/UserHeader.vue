<template>
  <header class="top-bar">
    <div class="welcome-message">
      <h1>{{ pageTitle }}</h1>
      <p class="subtitle">{{ pageSubtitle }}</p>
    </div>
    <div class="top-bar-actions">
      <button class="notification-btn" aria-label="Notifications">
        <i class="bi bi-bell"></i>
        <span class="notification-badge"></span>
      </button>
      
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
}

.notification-btn:hover {
  background-color: #FFFFFF;
  border-color: #D1D1D1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.notification-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 8px;
  height: 8px;
  background-color: var(--color-accent);
  border-radius: 50%;
  border: 1.5px solid var(--color-card);
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
