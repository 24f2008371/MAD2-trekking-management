<template>
  <div class="auth-card-container">
    <div class="light-card p-4 p-sm-5 text-center position-relative">
      <!-- Centered TrekMate Logo inside the Card with Inline Back Button -->
      <div class="logo-section mb-4 position-relative">
        <!-- Chevron Back to Home Button -->
        <router-link to="/" class="btn-back-chevron" title="Back to Home">
          <i class="bi bi-chevron-left"></i>
        </router-link>

        <div class="d-inline-flex align-items-center gap-2 mb-2">
          <div class="logo-icon-box">
            <i class="bi bi-compass-fill"></i>
          </div>
          <span class="logo-text font-heading">TrekMate</span>
        </div>
        <div class="gradient-underline mx-auto"></div>
      </div>

      <!-- Animated Pill Switcher (Centered & compact) -->
      <div class="pill-switcher mb-4 mx-auto">
        <!-- Sliding active background indicator -->
        <div 
          class="slider-indicator" 
          :class="{ 'slide-register': activeTab === 'register' }"
        ></div>
        
        <button 
          type="button" 
          class="switch-btn" 
          :class="{ active: activeTab === 'login' }"
          @click="changeTab('login')"
        >
          Sign In
        </button>
        <button 
          type="button" 
          class="switch-btn" 
          :class="{ active: activeTab === 'register' }"
          @click="changeTab('register')"
        >
          Register
        </button>
      </div>

      <!-- Form Slot -->
      <div class="form-slot">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  activeTab: {
    type: String,
    required: true,
    default: 'login'
  }
})

const emit = defineEmits(['update:activeTab'])

const changeTab = (tab) => {
  emit('update:activeTab', tab)
}
</script>

<style scoped>
.auth-card-container {
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
}

.light-card {
  background: #ffffff !important;
  border: 1px solid rgba(15, 23, 42, 0.06) !important;
  border-radius: 24px;
  box-shadow: 0 20px 45px rgba(15, 23, 42, 0.12);
  color: var(--text-dark, #111827);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

@media (max-width: 575.98px) {
  .light-card {
    padding: 24px !important;
  }
}

/* Logo Details */
.logo-icon-box {
  width: 32px;
  height: 32px;
  background: var(--gradient-orange);
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(255, 107, 53, 0.3);
}

.logo-icon-box i {
  color: white;
  font-size: 1.05rem;
}

.logo-text {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: #111827;
}

.gradient-underline {
  width: 60px;
  height: 2.5px;
  background: linear-gradient(90deg, transparent 0%, #FF6B35 50%, transparent 100%);
  border-radius: 2px;
}

/* Pill Switcher */
.pill-switcher {
  position: relative;
  background: rgba(15, 23, 42, 0.05);
  border: 1px solid rgba(15, 23, 42, 0.03);
  padding: 4px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 220px;
}

.slider-indicator {
  position: absolute;
  top: 4px;
  bottom: 4px;
  left: 4px;
  width: calc(50% - 4px);
  background: #ffffff;
  border: 1px solid rgba(15, 23, 42, 0.05);
  border-radius: 9px;
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08);
  transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  pointer-events: none;
  z-index: 0;
}

.slider-indicator.slide-register {
  transform: translateX(100%);
}

.switch-btn {
  flex: 1;
  background: none;
  border: none;
  color: #6B7280;
  padding: 8px 10px;
  font-size: 0.825rem;
  font-weight: 600;
  border-radius: 9px;
  cursor: pointer;
  transition: color 0.3s ease;
  z-index: 1;
  position: relative;
}

.switch-btn.active {
  color: #111827;
}

/* Back Chevron Button */
.btn-back-chevron {
  position: absolute;
  left: 0;
  top: 10px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  color: #94A3B8;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  text-decoration: none;
  z-index: 10;
}

.btn-back-chevron:hover {
  background: rgba(15, 23, 42, 0.04);
  color: #FF6B35;
  transform: translateX(-2px);
}

.btn-back-chevron i {
  font-size: 1.15rem;
  line-height: 1;
}
</style>
