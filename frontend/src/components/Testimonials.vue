<template>
  <section class="testimonials-section py-6 position-relative">
    <!-- Mountain Background Overlay Decor -->
    <div class="testimonials-bg-image"></div>
    <div class="testimonials-overlay"></div>

    <div class="container position-relative z-2">
      <div class="text-center mb-5 max-w-600 mx-auto">
        <h6 class="text-uppercase tracking-wider fw-bold text-gradient-accent mb-2">Testimonials</h6>
        <h2 class="section-title text-white font-heading">
          What Our Trekkers Say
        </h2>
        <p class="text-white-50">
          Real stories from real travelers who went on wild adventures with TrekMate.
        </p>
      </div>

      <div class="row justify-content-center">
        <div class="col-lg-8">
          <!-- Bootstrap Carousel -->
          <div id="testimonialCarousel" class="carousel slide" data-bs-ride="carousel">
            <!-- Carousel Indicators -->
            <div class="carousel-indicators mb-n5">
              <button
                type="button"
                data-bs-target="#testimonialCarousel"
                data-bs-slide-to="0"
                class="active"
                aria-current="true"
                aria-label="Slide 1"
              ></button>
              <button
                type="button"
                data-bs-target="#testimonialCarousel"
                data-bs-slide-to="1"
                aria-label="Slide 2"
              ></button>
              <button
                type="button"
                data-bs-target="#testimonialCarousel"
                data-bs-slide-to="2"
                aria-label="Slide 3"
              ></button>
            </div>

            <!-- Carousel Slides -->
            <div class="carousel-inner py-3">
              <!-- Slide 1 -->
              <div class="carousel-item active">
                <div class="glass-card testimonial-card p-5 text-center mx-auto text-white">
                  <!-- Star Rating -->
                  <div class="stars mb-4">
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                  </div>
                  <!-- Review Text -->
                  <blockquote class="blockquote-custom mb-4 font-heading">
                    "Trekking the Kedarkantha Peak with TrekMate was the best decision of my year. The guides were extremely friendly, safety standards were high-class, and the views were simply out of this world. Highly recommend!"
                  </blockquote>
                  <!-- User Info -->
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <img
                      src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&h=120&q=80"
                      alt="Aisha Sharma"
                      class="rounded-circle profile-img border border-2 border-white shadow-sm"
                    />
                    <div class="text-start">
                      <h5 class="reviewer-name font-heading mb-0">Aisha Sharma</h5>
                      <span class="reviewer-title text-white-50">Mumbai, India</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Slide 2 -->
              <div class="carousel-item">
                <div class="glass-card testimonial-card p-5 text-center mx-auto text-white">
                  <div class="stars mb-4">
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                  </div>
                  <blockquote class="blockquote-custom mb-4 font-heading">
                    "The medical support during the Roopkund expedition was outstanding. I suffered a minor bout of altitude sickness, but the guide squad managed my oxygen and pulse checks so efficiently I recovered and summited safely."
                  </blockquote>
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <img
                      src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&h=120&q=80"
                      alt="Rohan Verma"
                      class="rounded-circle profile-img border border-2 border-white shadow-sm"
                    />
                    <div class="text-start">
                      <h5 class="reviewer-name font-heading mb-0">Rohan Verma</h5>
                      <span class="reviewer-title text-white-50">Delhi, India</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Slide 3 -->
              <div class="carousel-item">
                <div class="glass-card testimonial-card p-5 text-center mx-auto text-white">
                  <div class="stars mb-4">
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                    <i class="bi bi-star-fill text-orange"></i>
                  </div>
                  <blockquote class="blockquote-custom mb-4 font-heading">
                    "I appreciated the zero-waste policy TrekMate strictly enforces. We hiked through pristine trails and camped at the cleanest sites. Incredible effort by the crew to protect our environment while offering luxury camps."
                  </blockquote>
                  <div class="d-flex align-items-center justify-content-center gap-3">
                    <img
                      src="https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&h=120&q=80"
                      alt="Elena Petrova"
                      class="rounded-circle profile-img border border-2 border-white shadow-sm"
                    />
                    <div class="text-start">
                      <h5 class="reviewer-name font-heading mb-0">Elena Petrova</h5>
                      <span class="reviewer-title text-white-50">Munich, Germany</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Controls -->
            <button class="carousel-control-prev" type="button" data-bs-target="#testimonialCarousel" data-bs-slide="prev">
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#testimonialCarousel" data-bs-slide="next">
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Next</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
</script>

<style scoped>
.testimonials-section {
  padding-top: 80px;
  padding-bottom: 120px;
  min-height: 550px;
  overflow: hidden;
}

.testimonials-bg-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('https://images.unsplash.com/photo-1482862549707-f63cb32c5fd9?auto=format&fit=crop&w=1920&q=80');
  background-size: cover;
  background-position: center;
  z-index: 1;
}

.testimonials-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(15, 23, 42, 0.85) 100%);
  z-index: 1;
}

.z-2 {
  z-index: 2;
}

.max-w-600 {
  max-width: 600px;
}

.text-gradient-accent {
  color: var(--accent-orange);
  letter-spacing: 2px;
  font-size: 0.85rem;
}

.text-orange {
  color: var(--accent-orange);
}

.testimonial-card {
  max-width: 700px;
  background: rgba(30, 41, 59, 0.45) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border-radius: var(--radius-lg);
}

.testimonial-card:hover {
  transform: none;
}

.stars i {
  font-size: 1.25rem;
  margin: 0 2px;
}

.blockquote-custom {
  font-size: clamp(1.1rem, 1.8vw, 1.45rem);
  font-weight: 500;
  line-height: 1.6;
  font-style: italic;
}

.profile-img {
  width: 65px;
  height: 65px;
  object-fit: cover;
}

.reviewer-name {
  font-size: 1.15rem;
  font-weight: 600;
}

.reviewer-title {
  font-size: 0.85rem;
}

.carousel-indicators {
  bottom: -40px;
}

.carousel-indicators button {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
}

.carousel-indicators button.active {
  background-color: var(--accent-orange);
}

.carousel-control-prev,
.carousel-control-next {
  width: 5%;
}

@media (max-width: 767.98px) {
  .testimonial-card {
    padding: 30px 20px !important;
  }
}
</style>
