<template>
  <nav
    class="navbar navbar-expand-lg sticky-top transition-navbar navbar-dark"
    :class="{ 'navbar-scrolled-dark': isScrolled, 'bg-transparent': !isScrolled }"
  >
    <div class="container">
      <!-- Logo -->
      <a class="navbar-brand d-flex align-items-center" href="#">
        <i class="bi bi-mountain-fill logo-icon me-2 text-orange"></i>
        <span class="logo-text font-heading text-white">TrekMate</span>
      </a>

      <!-- Responsive Mobile Toggle -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navigation Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mx-auto text-center py-3 py-lg-0">
          <li class="nav-item">
            <a class="nav-link px-3 font-heading" :class="{ active: activeSection === 'home' }" href="#home">Home</a>
          </li>
          <li class="nav-item">
            <a class="nav-link px-3 font-heading" :class="{ active: activeSection === 'treks' }" href="#treks">Treks</a>
          </li>
          <li class="nav-item">
            <a class="nav-link px-3 font-heading" :class="{ active: activeSection === 'about' }" href="#about">About</a>
          </li>
          <li class="nav-item">
            <a class="nav-link px-3 font-heading" :class="{ active: activeSection === 'contact' }" href="#contact">Contact</a>
          </li>
        </ul>

        <!-- Action Buttons -->
        <div class="d-flex flex-column flex-lg-row align-items-center justify-content-center gap-2">
          <router-link to="/auth/login" class="btn-nav-login px-4 py-2 font-heading text-white">
            Login
          </router-link>
          <router-link to="/auth/register" class="btn-premium-orange px-4 py-2 text-decoration-none">
            Register
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const activeSection = ref('home')

const handleScroll = () => {
  // Toggle scrolled navbar state
  if (window.scrollY > 50) {
    isScrolled.value = true
  } else {
    isScrolled.value = false
  }

  // Bottom scroll check for Footer / Contact section
  if ((window.innerHeight + window.scrollY) >= document.documentElement.scrollHeight - 60) {
    activeSection.value = 'contact'
    return
  }

  // Scrollspy logic
  const sections = ['home', 'treks', 'about', 'contact']
  let currentSection = 'home'
  
  for (const sectionId of sections) {
    const el = document.getElementById(sectionId)
    if (el) {
      const rect = el.getBoundingClientRect()
      if (rect.top <= 120) {
        currentSection = sectionId
      }
    }
  }
  activeSection.value = currentSection
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.transition-navbar {
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  padding-top: 20px;
  padding-bottom: 20px;
}

.navbar-scrolled-dark {
  padding-top: 12px;
  padding-bottom: 12px;
}

.logo-icon {
  font-size: 1.8rem;
  transition: var(--transition-smooth);
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.nav-link {
  font-weight: 600;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.8) !important;
  transition: var(--transition-smooth);
  position: relative;
}

.nav-link.active,
.nav-link:hover {
  color: var(--accent-orange) !important;
}

/* Hover line effect */
.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 15px;
  right: 15px;
  height: 2px;
  background-color: var(--accent-orange);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.nav-link:hover::after,
.nav-link.active::after {
  transform: scaleX(1);
}

.btn-nav-login {
  font-weight: 600;
  text-decoration: none;
  transition: var(--transition-smooth);
}

.btn-nav-login:hover {
  color: var(--accent-orange) !important;
}

@media (max-width: 991.98px) {
  .navbar-collapse {
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(10px);
    border-radius: var(--radius-md);
    padding: 20px;
    margin-top: 15px;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
}
</style>
