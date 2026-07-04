<template>
  <section class="gallery-section py-6 bg-white">
    <div class="container">
      <div class="text-center mb-5 max-w-600 mx-auto">
        <h6 class="text-uppercase text-blue tracking-wider fw-bold mb-2">Our Scrapbook</h6>
        <h2 class="section-title text-navy font-heading">
          Moments From the Wilderness
        </h2>
        <p class="text-muted">
          A glimpse into the breathtaking vistas, camaraderie, and peaceful campsites of our past expeditions.
        </p>
      </div>

      <!-- Masonry Grid -->
      <div class="masonry-grid">
        <div v-for="item in galleryItems" :key="item.id" class="masonry-item mb-4 overflow-hidden position-relative">
          <img :src="item.image" :alt="item.title" class="img-fluid w-100 h-100 object-fit-cover" />
          <div class="gallery-info-overlay d-flex flex-column justify-content-end p-4">
            <span class="gallery-tag text-uppercase mb-1 font-heading">{{ item.category }}</span>
            <h4 class="gallery-title text-white font-heading mb-0">{{ item.title }}</h4>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const galleryItems = ref([
  {
    id: 1,
    title: 'Majestic Peaks',
    category: 'Mountains',
    image: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 2,
    title: 'Under the Stars',
    category: 'Camping',
    image: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 3,
    title: 'Golden Hour Peak',
    category: 'Sunrise',
    image: 'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 4,
    title: 'Winter Wonderland',
    category: 'Snow',
    image: 'https://images.unsplash.com/photo-1482862549707-f63cb32c5fd9?auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 5,
    title: 'Glacial Flow',
    category: 'Rivers',
    image: 'https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 6,
    title: 'Summit Victory',
    category: 'Adventure',
    image: 'https://images.unsplash.com/photo-1527004013197-933c4bb611b3?auto=format&fit=crop&w=800&q=80'
  }
])
</script>

<style scoped>
.gallery-section {
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

/* Masonry Column Count Layout */
.masonry-grid {
  column-count: 3;
  column-gap: 1.5rem;
}

.masonry-item {
  break-inside: avoid;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-smooth);
  cursor: pointer;
}

.masonry-item img {
  display: block;
  width: 100%;
  transition: transform 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.gallery-info-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, rgba(15, 23, 42, 0.8) 0%, rgba(15, 23, 42, 0) 50%);
  opacity: 0;
  transition: var(--transition-smooth);
}

.gallery-tag {
  color: var(--accent-orange);
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.gallery-title {
  font-size: 1.25rem;
  font-weight: 600;
}

/* Hover Zoom & Info overlay reveal */
.masonry-item:hover img {
  transform: scale(1.08);
}

.masonry-item:hover .gallery-info-overlay {
  opacity: 1;
}

.masonry-item:hover {
  box-shadow: 0 15px 30px rgba(15, 23, 42, 0.1), 0 0 15px rgba(59, 130, 246, 0.1);
}

@media (max-width: 991.98px) {
  .masonry-grid {
    column-count: 2;
  }
}

@media (max-width: 575.98px) {
  .masonry-grid {
    column-count: 1;
  }
}
</style>
