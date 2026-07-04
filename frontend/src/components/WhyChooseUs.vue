<template>
  <section id="about" class="why-choose-us py-6 bg-light-slate">
    <div class="container">
      <!-- Section Header -->
      <div class="text-center mb-5 max-w-700 mx-auto">
        <h6 class="text-uppercase text-blue tracking-wider fw-bold mb-2">Our Standard</h6>
        <h2 class="section-title text-navy font-heading fw-bold mb-3">
          Setting the Benchmark in Outdoors
        </h2>
        <p class="text-muted fs-6">
          We take extreme care in organizing our expeditions. No shortcuts, no compromises. Just pure, safe, and unforgettable wilderness experiences.
        </p>
      </div>

      <!-- 4 Column Grid of Premium Standards -->
      <div class="row g-4">
        <div 
          v-for="(item, index) in standards" 
          :key="index" 
          class="col-md-6 col-lg-3"
        >
          <div class="standard-card h-100 rounded-4 bg-white p-3 border-0 shadow-sm transition-all hover-up">
            <!-- Image Frame (Vibrant, Clear, No Overlays) -->
            <div class="card-image-frame rounded-3 overflow-hidden mb-3">
              <img :src="item.image" :alt="item.title" class="w-100 h-100 object-fit-cover img-zoom" />
            </div>

            <!-- Card Content -->
            <div class="card-content">
              <div class="d-flex align-items-center gap-2 mb-2">
                <div class="icon-badge d-flex align-items-center justify-content-center rounded-3 bg-light-orange text-orange">
                  <i class="bi" :class="item.icon"></i>
                </div>
                <h4 class="font-heading mb-0 text-navy fw-bold fs-6">{{ item.title }}</h4>
              </div>
              
              <p class="text-muted text-xs line-height-relaxed mb-3">
                {{ item.description }}
              </p>

              <!-- Highlights -->
              <ul class="list-unstyled d-flex flex-column gap-2 border-top border-light pt-3 mt-2 text-navy text-xs">
                <li v-for="(bullet, bIdx) in item.bullets" :key="bIdx" class="d-flex align-items-start gap-2">
                  <i class="bi bi-check-lg text-orange mt-0.5"></i>
                  <span>{{ bullet }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import guideImg from '../assets/images/guide.png'
import medicalImg from '../assets/images/medical.png'
import trailImg from '../assets/images/trail.png'
import pricingImg from '../assets/images/pricing.png'

const standards = ref([
  {
    title: 'Certified Guides',
    icon: 'bi-award',
    image: guideImg,
    bullets: [
      'NIM / HMI certified experts',
      'Red Cross first-aid trained',
      'Bilingual local specialists'
    ],
    description: 'Every guide is certified by premier mountaineering institutes and carries extensive field rescue training.'
  },
  {
    title: 'Medical Safety',
    icon: 'bi-heart-pulse',
    image: medicalImg,
    bullets: [
      'Twice daily oximeter audits',
      'Oxygen & altitude gear on trail',
      'Direct base medical connections'
    ],
    description: 'We carry full high-altitude medical support kits, oxygen, and satellite links on every expedition.'
  },
  {
    title: 'Scouted Routes',
    icon: 'bi-compass',
    image: trailImg,
    bullets: [
      'Pre-season campsite audits',
      'Water source quality checks',
      'Real-time weather routing'
    ],
    description: 'We map, scout, and audit every route before our teams head out. Zero guesswork on the trail.'
  },
  {
    title: 'Transparent Value',
    icon: 'bi-tags',
    image: pricingImg,
    bullets: [
      'All permits & taxes included',
      'No surprise campsite fees',
      'Flexible reschedule policies'
    ],
    description: 'Clear cancellation terms, full gear rental transparency, and zero hidden checkout surcharges.'
  }
])
</script>

<style scoped>
.why-choose-us {
  padding-top: 80px;
  padding-bottom: 80px;
}

.max-w-700 {
  max-width: 700px;
}

.tracking-wider {
  letter-spacing: 2px;
  font-size: 0.85rem;
}

/* Card Design styling */
.standard-card {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  border: 1px solid rgba(15, 23, 42, 0.04) !important;
}

.hover-up:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08), 0 0 20px rgba(59, 130, 246, 0.05) !important;
  border-color: rgba(59, 130, 246, 0.15) !important;
}

.card-image-frame {
  height: 180px;
  width: 100%;
  position: relative;
}

.img-zoom {
  transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

.hover-up:hover .img-zoom {
  transform: scale(1.08);
}

.icon-badge {
  width: 32px;
  height: 32px;
  font-size: 1rem;
}

.bg-light-orange {
  background-color: rgba(255, 107, 53, 0.1);
}

.text-orange {
  color: var(--accent-orange);
}

.text-xs {
  font-size: 0.8rem;
}

.line-height-relaxed {
  line-height: 1.5;
}

.border-light {
  border-color: rgba(15, 23, 42, 0.06) !important;
}
</style>
