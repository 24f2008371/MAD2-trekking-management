<template>
  <header id="home" class="hero-section d-flex align-items-center position-relative overflow-hidden">
    <!-- Dark Gradient Overlay -->
    <div class="hero-overlay"></div>

    <div class="container position-relative z-2 py-5 text-center text-lg-start">
      <div class="row align-items-center min-vh-75 mt-5">
        <div class="col-lg-7 animate-fade-in-up">
          <!-- Premium Badge -->
          <div class="badge-premium mb-3 d-inline-flex align-items-center gap-2">
            <span class="pulse-dot"></span>
            <span class="text-uppercase tracking-wider text-white-50">Premium Adventure Travel</span>
          </div>

          <!-- Headings -->
          <h1 class="hero-title text-white mb-4">
            Explore the World <br />
            <span class="text-gradient">One Trek</span> at a Time
          </h1>

          <p class="hero-subtitle text-white-50 mb-5 max-w-600">
            Discover breathtaking adventures, challenge yourself, and create unforgettable trekking experiences. Handcrafted journeys with certified local guides.
          </p>

          <!-- Action Buttons -->
          <div class="d-flex flex-column flex-sm-row justify-content-center justify-content-lg-start gap-3">
            <a href="#treks" class="btn-premium-orange d-flex align-items-center justify-content-center gap-2 text-decoration-none px-4 py-3">
              Explore Treks <i class="bi bi-arrow-right-short fs-5"></i>
            </a>
            <a href="#about" class="btn-premium-outline d-flex align-items-center justify-content-center gap-2 text-decoration-none px-4 py-3">
              Learn More
            </a>
          </div>
        </div>

        <!-- Right Side: Trek of the Month Card -->
        <div class="col-lg-5 animate-fade-in-up delay-1 mt-5 mt-lg-0">
          <div class="glass-panel trek-month-card position-relative overflow-hidden p-4 text-white">
            <!-- Glowing Accent Border -->
            <div class="glow-effect"></div>
            
            <div class="card-header-badge mb-3 d-flex justify-content-between align-items-center">
              <span class="badge-trending text-uppercase tracking-wider text-xs">Trek of the Month</span>
              <span class="rating-badge d-flex align-items-center gap-1 text-sm">
                <i class="bi bi-star-fill text-warning"></i> 4.9 <span class="text-white-50">(128)</span>
              </span>
            </div>

            <!-- Trek Preview Image -->
            <div class="trek-preview-img-wrapper position-relative rounded-3 overflow-hidden mb-3">
              <img src="http://127.0.0.1:5000/static/uploads/1783458911_weichao-deng-eyn0LjpNWV4-unsplash.avif" alt="Everest Base Camp" class="img-fluid w-100 h-100 object-fit-cover trek-preview-img" />
              <span class="difficulty-tag position-absolute top-2 start-2 text-xs">Hard</span>
              <span class="price-tag position-absolute bottom-2 end-2 font-heading">₹48,000</span>
            </div>

            <!-- Trek Title & Details -->
            <h4 class="font-heading mb-1">Everest Base Camp</h4>
            <p class="text-white-50 text-sm mb-3 d-flex align-items-center gap-1">
              <i class="bi bi-geo-alt-fill text-orange"></i> Khumbu Valley, Nepal • 12 Days
            </p>

            <!-- Slots Progress Bar -->
            <div class="mb-4">
              <div class="d-flex justify-content-between text-xs text-white-50 mb-1">
                <span>Slots Booked</span>
                <span class="text-orange fw-semibold">Only {{ slotsLeft }} left!</span>
              </div>
              <div class="progress bg-white-10" style="height: 6px;">
                <div class="progress-bar progress-bar-orange" role="progressbar" :style="{ width: bookedPercentage + '%' }" :aria-valuenow="bookedPercentage" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            </div>

            <!-- Guide and CTA -->
            <div class="d-flex align-items-center justify-content-between gap-3 pt-2 border-top border-white-10">
              <div class="d-flex align-items-center gap-2">
                <div class="guide-avatar-wrapper position-relative">
                  <img :src="guideAvatarUrl" alt="Guide" class="rounded-circle guide-avatar" style="width: 38px; height: 38px; object-fit: cover;" />
                  <span class="status-indicator position-absolute bottom-0 end-0 bg-success border border-dark rounded-circle" style="width: 10px; height: 10px;"></span>
                </div>
                <div>
                  <span class="d-block text-xs text-white-50">Lead Guide</span>
                  <span class="text-sm fw-semibold">{{ guideName }}</span>
                </div>
              </div>
              
              <a href="#treks" class="btn-premium-orange px-4 py-2 text-sm text-decoration-none d-flex align-items-center gap-2">
                Explore Spot <i class="bi bi-arrow-right-short fs-5"></i>
              </a>
            </div>
          </div>
        </div>
      </div>


    </div>
  </header>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api/api.js'

const guideName = ref('Passang Sherpa')
const slotsLeft = ref(2)
const slotsBooked = ref(8)
const totalSlots = ref(10)

const guideAvatarUrl = computed(() => {
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(guideName.value)}&background=ff6b35&color=fff&bold=true`
})

const bookedPercentage = computed(() => {
  if (totalSlots.value === 0) return 0
  return (slotsBooked.value / totalSlots.value) * 100
})

onMounted(async () => {
  try {
    const response = await api.get('/treks')
    if (response.data && response.data.success) {
      const ebc = response.data.data.find(t => t.name === 'Everest Base Camp')
      if (ebc) {
        if (ebc.staff_name) {
          guideName.value = ebc.staff_name
        }
        slotsLeft.value = ebc.slots
        totalSlots.value = ebc.total_slots || ebc.slots
        slotsBooked.value = totalSlots.value - ebc.slots
      }
    }
  } catch (error) {
    console.error('Error fetching EBC trek guide details:', error)
  }
})
</script>

<style scoped>
.hero-section {
  background-image: url('../assets/images/hero_bg.png');
  background-size: cover;
  background-position: center 30%;
  min-height: 100vh;
  margin-top: -80px;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.45) 60%, rgba(15, 23, 42, 0.9) 100%);
  z-index: 1;
}

.z-2 {
  z-index: 2;
}

.min-vh-75 {
  min-height: 65vh;
}

.badge-premium {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 8px 16px;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 2px;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background-color: var(--accent-orange);
  border-radius: 50%;
  box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.7);
  animation: pulse 1.6s infinite;
}

@keyframes pulse {
  0% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(255, 107, 53, 0.7);
  }
  70% {
    transform: scale(1);
    box-shadow: 0 0 0 8px rgba(255, 107, 53, 0);
  }
  100% {
    transform: scale(0.95);
    box-shadow: 0 0 0 0 rgba(255, 107, 53, 0);
  }
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  font-weight: 800;
  line-height: 1.15;
}

.text-gradient {
  background: linear-gradient(90deg, #FF6B35 0%, #FFA800 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle {
  font-size: clamp(1rem, 1.5vw, 1.25rem);
  line-height: 1.6;
  font-weight: 300;
}

.max-w-600 {
  max-width: 600px;
}

/* Floating Stats Section */
.stats-container {
  background: rgba(30, 41, 59, 0.4) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
}

.stat-icon-wrapper {
  background-color: rgba(255, 255, 255, 0.05);
  width: 55px;
  height: 55px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: var(--accent-orange);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.stat-icon-wrapper i {
  background: linear-gradient(135deg, var(--accent-orange) 0%, var(--accent-blue) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
}

.stat-label {
  font-size: 0.85rem;
  font-weight: 400;
}

.stat-divider {
  width: 1px;
  height: 45px;
  background-color: rgba(255, 255, 255, 0.1);
}

/* Trek of the Month Card styles */
.trek-month-card {
  background: rgba(15, 23, 42, 0.45) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border-radius: var(--radius-lg);
  box-shadow: var(--glass-shadow);
  transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.trek-month-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5), 0 0 25px rgba(255, 107, 53, 0.15) !important;
}

.glow-effect {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 107, 53, 0.05) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.badge-trending {
  background: linear-gradient(90deg, #FF6B35 0%, #FFA800 100%);
  padding: 6px 12px;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.7rem;
  letter-spacing: 1.5px;
  box-shadow: 0 4px 10px rgba(255, 107, 53, 0.3);
}

.rating-badge {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 4px 10px;
  border-radius: 50px;
  font-weight: 600;
}

.trek-preview-img-wrapper {
  height: 180px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.trek-preview-img {
  transition: transform 0.6s ease;
}

.trek-month-card:hover .trek-preview-img {
  transform: scale(1.05);
}

.difficulty-tag {
  background-color: rgba(220, 53, 69, 0.85);
  backdrop-filter: blur(4px);
  padding: 4px 10px;
  border-radius: 50px;
  font-weight: 600;
}

.price-tag {
  background-color: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--accent-orange);
}

.bg-white-10 {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.progress-bar-orange {
  background: linear-gradient(90deg, #FF6B35 0%, #FFA800 100%) !important;
}

.guide-avatar {
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.border-white-10 {
  border-color: rgba(255, 255, 255, 0.1) !important;
}

.text-xs {
  font-size: 0.75rem;
}

.text-sm {
  font-size: 0.85rem;
}

@media (max-width: 991.98px) {
  .hero-section {
    padding-top: 100px;
  }
}

@media (max-width: 575.98px) {
  .stats-container {
    padding: 25px;
  }
  .stat-item {
    width: 100%;
    justify-content: center;
  }
}
</style>
