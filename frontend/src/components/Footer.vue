<template>
  <footer id="contact" class="footer-section bg-navy text-white pt-6 pb-4 position-relative">
    <div class="container z-2 position-relative">
      <div class="row g-4 mb-5">
        <!-- Logo & Bio Column -->
        <div class="col-lg-5 col-md-6 mb-4 mb-lg-0">
          <div class="d-flex align-items-center mb-3">
            <i class="bi bi-mountain-fill footer-logo-icon me-2 text-accent"></i>
            <span class="footer-logo-text font-heading text-white">TrekMate</span>
          </div>
          <p class="footer-bio text-white-50 mb-4 pe-lg-4">
            Setting the benchmark in outdoor adventures and high-altitude Himalayan expeditions. Discover raw wilderness safely with certified local experts.
          </p>
          <!-- Social Icons -->
          <div class="d-flex gap-3">
            <a href="https://www.instagram.com/trekmate13/" class="social-link" aria-label="Instagram">
              <i class="bi bi-instagram"></i>
            </a>
            <a href="https://x.com/ridhisehgal2" class="social-link" aria-label="Twitter">
              <i class="bi bi-twitter-x"></i>
            </a>
          </div>
        </div>

        <!-- Quick Links Column -->
        <div class="col-lg-3 col-md-6 col-6 mb-4 mb-lg-0">
          <h5 class="footer-heading font-heading mb-3">Quick Links</h5>
          <ul class="list-unstyled footer-links d-flex flex-column gap-2">
            <li><a href="#home">Home</a></li>
            <li><a href="#treks">Treks</a></li>
            <li><a href="#about">About Us</a></li>
            <li><a href="#features">Services</a></li>
          </ul>
        </div>

        <!-- Contact Column -->
        <div class="col-lg-4 col-md-6 col-6">
          <h5 class="footer-heading font-heading mb-3">Contact</h5>
          <ul class="list-unstyled footer-contact d-flex flex-column gap-3 text-white-50">
            <li class="d-flex align-items-start gap-2">
              <i class="bi bi-geo-alt-fill text-accent mt-1"></i>
              <span>102, Alpine Peak Residency, Rishikesh, Uttarakhand, Pin-249201</span>
            </li>
            <li class="d-flex align-items-center gap-2">
              <i class="bi bi-envelope-fill text-accent"></i>
              <a href="mailto:info@trekmate.com" class="text-decoration-none text-white-50">info@trekmate.com</a>
            </li>
            <li class="d-flex align-items-center gap-2">
              <i class="bi bi-telephone-fill text-accent"></i>
              <a href="tel:+919876543210" class="text-decoration-none text-white-50">+91 98765 43210</a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Copyright Area -->
      <div class="border-top border-secondary-dark pt-4 text-center d-flex flex-column flex-md-row justify-content-between align-items-center text-white-50 text-xs">
        <p class="mb-0">&copy; 2026 TrekMate Adventures Private Limited. All rights reserved.</p>
        <div class="mt-2 mt-md-0">
          <span>Made by Ridhi Sehgal</span>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>

<style scoped>
.footer-section {
  padding-top: 80px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.bg-navy {
  background-color: var(--primary-navy) !important;
}

.text-accent {
  color: var(--accent-orange);
}

.border-secondary-dark {
  border-color: rgba(255, 255, 255, 0.08) !important;
}

.footer-logo-icon {
  font-size: 2rem;
}

.footer-logo-text {
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: 0.5px;
}

.footer-bio {
  font-size: 0.9rem;
  line-height: 1.6;
}

.footer-heading {
  font-size: 1.15rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #FFFFFF;
}

.footer-links a {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.95rem;
  transition: var(--transition-smooth);
}

.footer-links a:hover {
  color: var(--accent-orange);
  padding-left: 5px;
}

.footer-contact span, .footer-contact a {
  font-size: 0.9rem;
  line-height: 1.5;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1.1rem;
  transition: var(--transition-smooth);
  text-decoration: none;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.social-link:hover {
  background: var(--gradient-orange);
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
}

/* Newsletter styling */
.newsletter-form .form-control {
  font-size: 0.9rem;
}

.newsletter-input:focus {
  background-color: transparent !important;
  border-color: var(--accent-orange) !important;
  color: white !important;
  box-shadow: none;
}

.btn-accent-submit {
  width: 38px;
  height: 38px;
  background-color: var(--accent-orange);
  border: none;
  transition: var(--transition-smooth);
}

.btn-accent-submit:hover {
  background-color: var(--accent-orange-hover);
  transform: translateY(-50%) scale(1.05);
}

.end-1 {
  right: 6px;
}

.text-xs {
  font-size: 0.8rem;
}

.hover-text-white:hover {
  color: #FFFFFF !important;
}

@media (max-width: 767.98px) {
  .footer-section {
    padding-top: 60px;
  }
}
</style>
