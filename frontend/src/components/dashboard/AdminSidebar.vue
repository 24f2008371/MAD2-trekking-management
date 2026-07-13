<template>
  <aside class="sidebar" :class="{ collapsed: isCollapsed }">
    <!-- Brand Info -->
    <div class="sidebar-brand-wrapper d-flex align-items-center justify-content-between">
      <router-link to="/" class="sidebar-brand text-decoration-none" v-if="!isCollapsed">
        <span class="logo-text">Trek<span class="orange-text">Mate</span></span>
        <span class="logo-badge">Admin</span>
      </router-link>
      <router-link to="/" class="sidebar-brand text-decoration-none" v-else>
        <span class="logo-text orange-text">TM</span>
      </router-link>
    </div>

    <!-- Navigation Items -->
    <nav class="sidebar-nav mt-4">
      <router-link 
        v-for="item in navItems" 
        :key="item.name" 
        :to="item.path"
        class="nav-item" 
        active-class="active"
      >
        <span class="nav-icon" v-html="item.icon"></span>
        <span class="nav-label" v-if="!isCollapsed">{{ item.name }}</span>
      </router-link>
    </nav>

    <!-- Logout / Footer -->
    <div class="sidebar-footer">
      <a href="#" class="nav-item logout-btn" @click.prevent="$emit('logout')">
        <span class="nav-icon"><i class="bi bi-box-arrow-right"></i></span>
        <span class="nav-label" v-if="!isCollapsed">Logout</span>
      </a>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  isCollapsed: {
    type: Boolean,
    default: false
  }
})

defineEmits(['logout'])

const navItems = [
  { name: 'Dashboard', path: '/admin/dashboard', icon: '<i class="bi bi-grid"></i>' },
  { name: 'Treks', path: '/admin/treks', icon: '<i class="bi bi-compass"></i>' },
  { name: 'Trekking Staff', path: '/admin/staff', icon: '<i class="bi bi-person-badge"></i>' },
  { name: 'Users (Trekkers)', path: '/admin/users', icon: '<i class="bi bi-people"></i>' },
  { name: 'Bookings', path: '/admin/bookings', icon: '<i class="bi bi-journal-check"></i>' },
  { name: 'Search', path: '/admin/search', icon: '<i class="bi bi-search"></i>' },
  { name: 'Reports', path: '/admin/reports', icon: '<i class="bi bi-bar-chart-line"></i>' }
]
</script>

<style scoped>
.sidebar {
  width: 260px;
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
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 4px 0 16px rgba(15, 23, 42, 0.015);
}

.sidebar.collapsed {
  width: 78px;
  padding: 1.75rem 0.75rem;
}

.sidebar-brand-wrapper {
  height: 50px;
  padding: 0 0.5rem;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-text {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.25rem;
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
  margin-top: -0.25rem;
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

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 0.75rem 0;
  gap: 0;
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
</style>
