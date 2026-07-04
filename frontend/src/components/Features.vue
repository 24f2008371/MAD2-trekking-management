<template>
  <section id="features" class="features-section py-6 bg-light-slate">
    <div class="container">
      <div class="text-center mb-5 max-w-600 mx-auto">
        <h6 class="text-uppercase text-blue tracking-wider fw-bold mb-2">Our Services</h6>
        <h2 class="section-title text-navy font-heading">
          Why Trek With <span class="text-orange">TrekMate</span>?
        </h2>
        <p class="text-muted">
          We combine safety, adventure, and comfort to provide you with the most memorable wilderness experiences of your life.
        </p>
      </div>

      <div class="row g-4">
        <!-- Feature Card 1 -->
        <div class="col-md-6 col-lg-3">
          <div class="feature-card h-100 p-4 bg-white shadow-sm border-0 position-relative overflow-hidden">
            <div class="icon-container mb-4 icon-brand-glow">
              <i class="bi bi-shield-check"></i>
            </div>
            <h4 class="card-heading font-heading mb-3">Safe & Secure</h4>
            <p class="card-text text-muted mb-0">
              State-of-the-art safety gear, satellite communication, and highly trained personnel on every journey.
            </p>
          </div>
        </div>

        <!-- Feature Card 2 -->
        <div class="col-md-6 col-lg-3">
          <div class="feature-card h-100 p-4 bg-white shadow-sm border-0 position-relative overflow-hidden">
            <div class="icon-container mb-4 icon-brand-glow">
              <i class="bi bi-person-badge"></i>
            </div>
            <h4 class="card-heading font-heading mb-3">Expert Guides</h4>
            <p class="card-text text-muted mb-0">
              Local certified experts with decades of wilderness experience, safety rescue skills, and local tales.
            </p>
          </div>
        </div>

        <!-- Feature Card 3 -->
        <div class="col-md-6 col-lg-3">
          <div class="feature-card h-100 p-4 bg-white shadow-sm border-0 position-relative overflow-hidden">
            <div class="icon-container mb-4 icon-brand-glow">
              <i class="bi bi-map"></i>
            </div>
            <h4 class="card-heading font-heading mb-3">Best Destinations</h4>
            <p class="card-text text-muted mb-0">
              Meticulously planned trails to remote peaks, hidden valleys, alpine meadows, and majestic peaks.
            </p>
          </div>
        </div>

        <!-- Feature Card 4 -->
        <div class="col-md-6 col-lg-3">
          <div class="feature-card h-100 p-4 bg-white shadow-sm border-0 position-relative overflow-hidden">
            <div class="icon-container mb-4 icon-brand-glow">
              <i class="bi bi-headset"></i>
            </div>
            <h4 class="card-heading font-heading mb-3">24×7 Support</h4>
            <p class="card-text text-muted mb-0">
              Always-on support team to manage bookings, emergency situations, real-time trail updates, and custom queries.
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.features-section {
  padding-top: 80px;
  padding-bottom: 80px;
}

.max-w-600 {
  max-width: 600px;
}

.tracking-wider {
  letter-spacing: 2px;
  font-size: 0.85rem;
}

.feature-card {
  border-radius: var(--radius-lg);
  transition: var(--transition-smooth);
  cursor: default;
  z-index: 1;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-orange) 0%, var(--accent-blue) 100%);
  transform: scaleX(0);
  transition: var(--transition-smooth);
  transform-origin: left;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(15, 23, 42, 0.08), 0 0 15px rgba(59, 130, 246, 0.1) !important;
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.icon-container {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: var(--radius-md);
  font-size: 1.8rem;
}

.feature-card:hover .icon-container {
  background: linear-gradient(135deg, var(--accent-orange) 0%, var(--accent-blue) 100%);
  transform: translateY(-4px) scale(1.06);
  box-shadow: 0 8px 15px rgba(59, 130, 246, 0.2);
}

.feature-card:hover .icon-container i {
  -webkit-text-fill-color: white !important;
  color: white !important;
}

.card-heading {
  font-size: 1.25rem;
  color: var(--primary-navy);
  font-weight: 700;
}

.card-text {
  font-size: 0.9rem;
  line-height: 1.6;
}
</style>
