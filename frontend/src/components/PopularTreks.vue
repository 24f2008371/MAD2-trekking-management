<template>
  <section id="treks" class="popular-treks py-6 bg-light-slate">
    <div class="container">
      <div class="text-center mb-5 max-w-600 mx-auto">
        <h6 class="text-uppercase text-blue tracking-wider fw-bold mb-2">Featured Adventures</h6>
        <h2 class="section-title text-navy font-heading">
          Popular Trekking Expeditions
        </h2>
        <p class="text-muted">
          Join one of our scheduled departures to the highest peaks and most spectacular valley landscapes.
        </p>
      </div>

      <div class="row g-4">
        <!-- Trek Card -->
        <div v-for="trek in treks" :key="trek.id" class="col-md-6 col-lg-4">
          <div class="card h-100 trek-card border-0 shadow-sm overflow-hidden bg-white">
            <!-- Image & Badge Container -->
            <div class="position-relative overflow-hidden trek-img-container">
              <img :src="trek.image" :alt="trek.name" class="img-fluid trek-img w-100 h-100 object-fit-cover" />
              <!-- Difficulty Badge -->
              <span class="badge position-absolute top-3 start-3 px-3 py-2 rounded-pill font-heading" :class="difficultyClass(trek.difficulty)">
                {{ trek.difficulty }}
              </span>
              <!-- Duration Badge -->
              <span class="badge duration-badge position-absolute bottom-3 end-3 px-3 py-2 rounded-3 font-heading">
                <i class="bi bi-clock-history me-1 text-orange"></i> {{ trek.duration }}
              </span>
            </div>

            <!-- Card Body -->
            <div class="card-body p-4 d-flex flex-column justify-content-between">
              <div>
                <!-- Location -->
                <p class="trek-location text-muted mb-2 d-flex align-items-center gap-1">
                  <i class="bi bi-geo-alt-fill text-blue"></i> {{ trek.location }}
                </p>
                <!-- Title -->
                <h4 class="trek-title font-heading mb-3 text-navy">{{ trek.name }}</h4>
                <!-- Details -->
                <div class="d-flex justify-content-between align-items-center mb-4 py-2 border-top border-bottom border-light">
                  <div class="trek-detail">
                    <span class="d-block text-muted text-xs">Available Slots</span>
                    <span class="fw-semibold text-dark d-flex align-items-center gap-1">
                      <i class="bi bi-people text-orange"></i> {{ trek.slots }} left
                    </span>
                  </div>
                  <div class="trek-detail text-end">
                    <span class="d-block text-muted text-xs">Starting from</span>
                    <span class="trek-price font-heading">{{ trek.price }}</span>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="row g-2">
                <div class="col-6">
                  <button class="btn btn-outline-navy w-100 btn-view-details rounded-pill font-heading text-xs py-2">
                    View Details
                  </button>
                </div>
                <div class="col-6">
                  <button class="btn btn-premium-orange w-100 btn-book-now rounded-pill font-heading text-xs py-2">
                    Book Now
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
import trek1Img from '../assets/images/trek_1.png'
import trek2Img from '../assets/images/trek_2.png'
import trek3Img from '../assets/images/trek_3.png'
import trek4Img from '../assets/images/trek_4.png'

const treks = ref([
  {
    id: 1,
    name: 'Kedarkantha Winter Expedition',
    location: 'Garhwal Himalayas, Uttarakhand',
    difficulty: 'Easy-Moderate',
    duration: '6 Days',
    slots: 8,
    price: '₹8,500',
    image: trek1Img
  },
  {
    id: 2,
    name: 'Roopkund Lake Trail',
    location: 'Chamoli District, Uttarakhand',
    difficulty: 'Hard',
    duration: '8 Days',
    slots: 5,
    price: '₹14,200',
    image: trek2Img
  },
  {
    id: 3,
    name: 'Valley of Flowers Trek',
    location: 'West Himalayas, Uttarakhand',
    difficulty: 'Easy',
    duration: '6 Days',
    slots: 12,
    price: '₹9,800',
    image: trek3Img
  },
  {
    id: 4,
    name: 'Hampta Pass Crossing',
    location: 'Manali, Himachal Pradesh',
    difficulty: 'Moderate',
    duration: '5 Days',
    slots: 6,
    price: '₹10,500',
    image: trek4Img
  },
  {
    id: 5,
    name: 'Annapurna Base Camp',
    location: 'Gandaki Province, Nepal',
    difficulty: 'Hard',
    duration: '11 Days',
    slots: 4,
    price: '₹32,000',
    image: trek2Img
  },
  {
    id: 6,
    name: 'Har Ki Dun Valley',
    location: 'Uttarkashi, Uttarakhand',
    difficulty: 'Easy-Moderate',
    duration: '7 Days',
    slots: 10,
    price: '₹11,000',
    image: trek1Img
  }
])

const difficultyClass = (diff) => {
  if (diff === 'Easy') return 'bg-success text-white'
  if (diff === 'Easy-Moderate' || diff === 'Moderate') return 'bg-warning text-dark'
  return 'bg-danger text-white'
}
</script>

<style scoped>
.popular-treks {
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

.trek-card {
  border-radius: var(--radius-lg);
  transition: var(--transition-smooth);
  height: 100%;
}

.trek-card:hover {
  transform: translateY(-8px) scale(1.01);
  box-shadow: 0 15px 30px rgba(15, 23, 42, 0.1), 0 0 20px rgba(59, 130, 246, 0.15) !important;
}

.trek-img-container {
  height: 240px;
  border-top-left-radius: var(--radius-lg);
  border-top-right-radius: var(--radius-lg);
}

.trek-img {
  transition: transform 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.trek-card:hover .trek-img {
  transform: scale(1.1);
}

.top-3 {
  top: 1rem;
}

.start-3 {
  left: 1rem;
}

.bottom-3 {
  bottom: 1rem;
}

.end-3 {
  right: 1rem;
}

.duration-badge {
  background-color: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(5px);
  -webkit-backdrop-filter: blur(5px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.trek-location {
  font-size: 0.85rem;
  font-weight: 500;
}

.trek-title {
  font-weight: 700;
  font-size: 1.3rem;
  line-height: 1.4;
  height: 54px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.text-xs {
  font-size: 0.75rem;
}

.trek-price {
  font-size: 1.35rem;
  font-weight: 800;
  color: var(--accent-orange);
}

.btn-view-details {
  border-color: var(--primary-navy);
  color: var(--primary-navy);
  font-weight: 600;
  transition: var(--transition-smooth);
}

.btn-view-details:hover {
  background-color: var(--primary-navy);
  color: white;
  box-shadow: 0 0 15px rgba(59, 130, 246, 0.3);
}

.btn-book-now {
  padding-top: 10px;
  padding-bottom: 10px;
  border-radius: 30px;
}
</style>
