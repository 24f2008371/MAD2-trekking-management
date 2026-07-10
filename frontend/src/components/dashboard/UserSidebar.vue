<template>
  <aside class="sidebar">
    <router-link to="/" class="sidebar-brand text-decoration-none">
      <span class="logo-text">Trek<span class="orange-text">Mate</span></span>
      <span class="logo-badge">User</span>
    </router-link>

    <nav class="sidebar-nav">
      <a 
        v-for="item in navItems" 
        :key="item.name" 
        href="#"
        class="nav-item" 
        :class="{ active: activeTab === item.id }"
        @click.prevent="$emit('select-tab', item.id)"
      >
        <span class="nav-icon" v-html="item.icon"></span>
        <span class="nav-label">{{ item.name }}</span>
      </a>
    </nav>

    <div class="sidebar-footer">
      <a href="#" class="nav-item logout-btn" @click.prevent="$emit('logout')">
        <span class="nav-icon"><i class="bi bi-box-arrow-right"></i></span>
        <span class="nav-label">Logout</span>
      </a>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  activeTab: {
    type: String,
    required: true
  },
  navItems: {
    type: Array,
    required: true
  }
})

defineEmits(['select-tab', 'logout'])
</script>

<style scoped>
.sidebar {
  width: 240px;
  background-color: var(--color-card);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  z-index: 100;
  padding: 2rem 1.25rem;
}

.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-left: 0.75rem;
  margin-bottom: 3rem;
}

.logo-text {
  font-family: 'Montserrat', sans-serif;
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--color-text-primary);
  letter-spacing: -0.03em;
}

.orange-text {
  color: var(--color-accent);
}

.logo-badge {
  font-size: 0.65rem;
  font-weight: 700;
  background-color: var(--color-accent-light);
  color: var(--color-accent);
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
  color: var(--color-text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.925rem;
  border-radius: 10px;
  transition: all 0.2s ease-in-out;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background-color: #F5F5F3;
  color: var(--color-text-primary);
}

.nav-item.active {
  background-color: var(--color-accent-light);
  color: var(--color-accent);
  border-left-color: var(--color-accent);
  font-weight: 600;
}

.nav-icon {
  font-size: 1.1rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.sidebar-footer {
  margin-top: auto;
  border-top: 1px solid var(--color-border);
  padding-top: 1.5rem;
}

.logout-btn {
  color: #EF4444;
}
.logout-btn:hover {
  background-color: #FEE2E2;
  color: #DC2626;
}
</style>
