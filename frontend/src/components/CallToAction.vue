<template>
  <section class="cta-section py-6 position-relative overflow-hidden">
    <!-- Circle Decors -->
    <div class="cta-circle-1"></div>
    <div class="cta-circle-2"></div>

    <div class="container position-relative z-2 text-center text-white py-4">
      <div class="max-w-700 mx-auto">
        <h6 class="text-uppercase tracking-wider fw-bold text-gradient-accent mb-3">Begin Your Journey</h6>
        <h2 class="cta-heading font-heading mb-4">
          Ready For Your Next Adventure?
        </h2>
        <p class="cta-text text-white-50 mb-5">
          Join thousands of other adventure seekers today. Sign up, reserve slots on our scheduled departures, or customize your dream trail from scratch.
        </p>

        <!-- CTA Buttons -->
        <div class="d-flex flex-column flex-sm-row justify-content-center align-items-center gap-3">
          <router-link to="/auth/login" class="btn-premium-orange px-5 py-3 text-decoration-none">
            Start Exploring
          </router-link>
          <router-link to="/auth/register" class="btn-premium-outline px-5 py-3 text-decoration-none">
            Register Today
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.cta-section {
  background: linear-gradient(135deg, var(--primary-navy) 0%, var(--secondary-slate) 100%);
  padding-top: 100px;
  padding-bottom: 100px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.max-w-700 {
  max-width: 700px;
}

.text-gradient-accent {
  color: var(--accent-orange);
  letter-spacing: 3px;
  font-size: 0.9rem;
}

.cta-heading {
  font-size: clamp(2rem, 4vw, 3.25rem);
  font-weight: 800;
  line-height: 1.25;
}

.cta-text {
  font-size: clamp(1rem, 1.25vw, 1.15rem);
  font-weight: 300;
  line-height: 1.7;
}

.cta-circle-1 {
  position: absolute;
  top: -150px;
  left: -150px;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.15) 0%, transparent 70%);
  z-index: 1;
}

.cta-circle-2 {
  position: absolute;
  bottom: -150px;
  right: -150px;
  width: 450px;
  height: 450px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 107, 53, 0.1) 0%, transparent 70%);
  z-index: 1;
}

.z-2 {
  z-index: 2;
}

@media (max-width: 575.98px) {
  .btn-premium-orange, .btn-premium-outline {
    width: 100%;
    text-align: center;
  }
}
</style>
