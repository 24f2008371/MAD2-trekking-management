<template>
  <div class="auth-page-wrapper d-flex align-items-center justify-content-center min-vh-100 p-3">
    <!-- Cinematic Zooming Background Image -->
    <div class="auth-bg-img"></div>
    
    <!-- Dark Gradient Overlay -->
    <div class="auth-overlay"></div>

    <!-- Centered Card Container (with bounce-up animation) -->
    <div class="auth-card-wrapper position-relative z-2">
      <AuthCard :activeTab="activeTab" @update:activeTab="handleTabChange">
        <transition name="form-fade" mode="out-in">
          <LoginForm v-if="activeTab === 'login'" />
          <RegisterForm v-else @auth-success="activeTab = 'login'" />
        </transition>
      </AuthCard>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AuthCard from '../components/AuthCard.vue'
import LoginForm from '../components/LoginForm.vue'
import RegisterForm from '../components/RegisterForm.vue'

const route = useRoute()
const router = useRouter()

const activeTab = ref(route.path.includes('register') ? 'register' : 'login')

watch(() => route.path, (newPath) => {
  activeTab.value = newPath.includes('register') ? 'register' : 'login'
})

const handleTabChange = (newTab) => {
  activeTab.value = newTab
  router.push(`/auth/${newTab}`)
}

onMounted(() => {
  activeTab.value = route.path.includes('register') ? 'register' : 'login'
})
</script>

<style scoped>
.auth-page-wrapper {
  width: 100vw;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

/* HD background image with cinematic slow zoom-out + blur-fade entrance */
.auth-bg-img {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('../assets/images/majestic_mountains.png');
  background-size: cover;
  background-position: center center;
  z-index: 0;
  animation: zoomBg 2.4s cubic-bezier(0.25, 1, 0.5, 1) forwards;
  transform-origin: center center;
}

@keyframes zoomBg {
  0% {
    transform: scale(1.08);
    filter: blur(4px);
  }
  100% {
    transform: scale(1);
    filter: blur(0);
  }
}

.auth-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.45) 0%, rgba(15, 23, 42, 0.25) 100%);
  z-index: 1;
}

/* Centered Card Bounce Entrance Animation */
.auth-card-wrapper {
  width: 100%;
  max-width: 520px;
  margin: 0 auto;
  z-index: 2;
  animation: cardEnter 0.85s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes cardEnter {
  0% {
    opacity: 0;
    transform: scale(0.92) translateY(24px);
  }
  100% {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.z-2 {
  z-index: 2;
}

/* Smooth route switching animations */
.form-fade-enter-active,
.form-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.form-fade-enter-from {
  opacity: 0;
  transform: translateY(15px);
}

.form-fade-leave-to {
  opacity: 0;
  transform: translateY(-15px);
}
</style>
