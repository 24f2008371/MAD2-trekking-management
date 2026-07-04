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

        <!-- Right Side: Interactive Planner Card -->
        <div class="col-lg-5 animate-fade-in-up delay-1 mt-5 mt-lg-0">
          <div class="glass-panel planner-card p-4 text-white">
            <h4 class="font-heading mb-3 d-flex align-items-center gap-2">
              <i class="bi bi-send-fill text-orange"></i> Plan Your Expedition
            </h4>
            <p class="text-white-50 text-sm mb-4">
              Enter your preferences to check real-time availability of certified trails.
            </p>
            <form @submit.prevent class="planner-form d-flex flex-column gap-3 text-start">
              <div>
                <label class="form-label text-xs text-white-50 text-uppercase fw-semibold tracking-wider mb-1">Destination</label>
                <div class="input-group">
                  <span class="input-group-text bg-transparent border-white-15 text-white-50"><i class="bi bi-geo-alt"></i></span>
                  <select class="form-select bg-transparent border-white-15 text-white">
                    <option value="" class="bg-navy-select text-white">All Locations</option>
                    <option value="uttarakhand" class="bg-navy-select text-white">Uttarakhand, India</option>
                    <option value="himachal" class="bg-navy-select text-white">Himachal Pradesh, India</option>
                    <option value="nepal" class="bg-navy-select text-white">Gandaki Province, Nepal</option>
                  </select>
                </div>
              </div>
              
              <div class="row g-2">
                <div class="col-6">
                  <label class="form-label text-xs text-white-50 text-uppercase fw-semibold tracking-wider mb-1">Difficulty</label>
                  <select class="form-select bg-transparent border-white-15 text-white">
                    <option value="" class="bg-navy-select text-white">Any Level</option>
                    <option value="easy" class="bg-navy-select text-white">Easy</option>
                    <option value="moderate" class="bg-navy-select text-white">Moderate</option>
                    <option value="hard" class="bg-navy-select text-white">Hard</option>
                  </select>
                </div>
                <div class="col-6">
                  <label class="form-label text-xs text-white-50 text-uppercase fw-semibold tracking-wider mb-1">Month</label>
                  <select class="form-select bg-transparent border-white-15 text-white">
                    <option value="" class="bg-navy-select text-white">Any Month</option>
                    <option value="july" class="bg-navy-select text-white">July 2026</option>
                    <option value="august" class="bg-navy-select text-white">August 2026</option>
                    <option value="september" class="bg-navy-select text-white">September 2026</option>
                  </select>
                </div>
              </div>

              <button type="submit" class="btn-premium-orange w-100 py-3 mt-2 d-flex align-items-center justify-content-center gap-2">
                Find My Trail <i class="bi bi-compass"></i>
              </button>
            </form>
          </div>
        </div>
      </div>


    </div>
  </header>
</template>

<script setup>
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

.planner-card {
  background: rgba(15, 23, 42, 0.45) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border-radius: var(--radius-lg);
  box-shadow: var(--glass-shadow);
}

.border-white-15 {
  border-color: rgba(255, 255, 255, 0.15) !important;
}

.bg-navy-select {
  background-color: var(--primary-navy) !important;
}

.text-xs {
  font-size: 0.75rem;
}

.text-sm {
  font-size: 0.85rem;
}

.form-select {
  background-color: rgba(30, 41, 59, 0.2);
  border-radius: var(--radius-sm);
  color: white !important;
  cursor: pointer;
}

.form-select:focus {
  border-color: var(--accent-orange);
  box-shadow: none;
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
