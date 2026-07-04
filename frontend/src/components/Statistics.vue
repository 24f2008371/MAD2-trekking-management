<template>
  <section class="statistics-section py-5 text-white position-relative overflow-hidden">
    <div class="stats-bg-decor"></div>
    <div class="container position-relative z-1">
      <div class="row g-4 text-center">
        <!-- Stat Item 1 -->
        <div class="col-6 col-lg-3">
          <div class="stat-counter-card">
            <div class="stat-icon-circle mx-auto mb-3">
              <i class="bi bi-geo-alt"></i>
            </div>
            <h2 class="counter-number font-heading mb-1">{{ animatedTreks }}+</h2>
            <p class="counter-label text-white-50 mb-0">Total Treks</p>
          </div>
        </div>

        <!-- Stat Item 2 -->
        <div class="col-6 col-lg-3">
          <div class="stat-counter-card">
            <div class="stat-icon-circle mx-auto mb-3">
              <i class="bi bi-emoji-smile"></i>
            </div>
            <h2 class="counter-number font-heading mb-1">{{ animatedTrekkers.toLocaleString() }}+</h2>
            <p class="counter-label text-white-50 mb-0">Happy Trekkers</p>
          </div>
        </div>

        <!-- Stat Item 3 -->
        <div class="col-6 col-lg-3">
          <div class="stat-counter-card">
            <div class="stat-icon-circle mx-auto mb-3">
              <i class="bi bi-people"></i>
            </div>
            <h2 class="counter-number font-heading mb-1">{{ animatedGuides }}+</h2>
            <p class="counter-label text-white-50 mb-0">Expert Guides</p>
          </div>
        </div>

        <!-- Stat Item 4 -->
        <div class="col-6 col-lg-3">
          <div class="stat-counter-card">
            <div class="stat-icon-circle mx-auto mb-3">
              <i class="bi bi-shield-check"></i>
            </div>
            <h2 class="counter-number font-heading mb-1">{{ animatedSafety }}%</h2>
            <p class="counter-label text-white-50 mb-0">Safety Record</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const animatedTreks = ref(0)
const animatedTrekkers = ref(0)
const animatedGuides = ref(0)
const animatedSafety = ref(0)

const animateValue = (refVar, start, end, duration) => {
  let startTimestamp = null
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp
    const progress = Math.min((timestamp - startTimestamp) / duration, 1)
    refVar.value = Math.floor(progress * (end - start) + start)
    if (progress < 1) {
      window.requestAnimationFrame(step)
    }
  }
  window.requestAnimationFrame(step)
}

onMounted(() => {
  animateValue(animatedTreks, 0, 100, 1500)
  animateValue(animatedTrekkers, 0, 5000, 1500)
  animateValue(animatedGuides, 0, 50, 1500)
  animateValue(animatedSafety, 0, 99, 1500)
})
</script>

<style scoped>
.statistics-section {
  background-color: var(--primary-navy);
  padding: 80px 0 !important;
}

.stats-bg-decor {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 80% 20%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
              radial-gradient(circle at 10% 80%, rgba(255, 107, 53, 0.15) 0%, transparent 40%);
  pointer-events: none;
}

.z-1 {
  z-index: 1;
}

.stat-icon-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  transition: var(--transition-smooth);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-icon-circle i {
  background: linear-gradient(135deg, var(--accent-orange) 0%, var(--accent-blue) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-counter-card:hover .stat-icon-circle {
  background: linear-gradient(135deg, var(--accent-orange) 0%, var(--accent-blue) 100%);
  transform: translateY(-5px);
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
}

.stat-counter-card:hover .stat-icon-circle i {
  -webkit-text-fill-color: white !important;
  color: white !important;
}

.counter-number {
  font-size: clamp(2rem, 4.5vw, 3.25rem);
  font-weight: 800;
  color: white;
}

.counter-label {
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: 0.5px;
}

@media (max-width: 767.98px) {
  .statistics-section {
    padding: 60px 0 !important;
  }
}
</style>
