<template>
  <div class="dashboard-container">
    <!-- Filter Bar -->
    <div class="filter-bar mb-4">
      <div class="search-input-wrapper">
        <i class="bi bi-search search-icon"></i>
        <input 
          :value="searchQuery" 
          @input="$emit('update:searchQuery', $event.target.value)"
          type="text" 
          placeholder="Search treks..." 
          class="search-control"
        />
      </div>
      <div class="filter-dropdowns">
        <div class="select-wrapper">
          <select 
            :value="difficultyFilter" 
            @change="$emit('update:difficultyFilter', $event.target.value)" 
            class="select-control"
          >
            <option value="All">Difficulty: All</option>
            <option value="Easy">Easy</option>
            <option value="Moderate">Moderate</option>
            <option value="Hard">Hard</option>
            <option value="Difficult">Difficult</option>
          </select>
          <i class="bi bi-chevron-down select-arrow"></i>
        </div>
        <div class="select-wrapper">
          <select 
            :value="locationFilter" 
            @change="$emit('update:locationFilter', $event.target.value)" 
            class="select-control"
          >
            <option value="All">Location: All</option>
            <option value="Nepal">Nepal</option>
            <option value="Uttarakhand">Uttarakhand</option>
            <option value="Himachal">Himachal</option>
            <option value="Sikkim">Sikkim</option>
          </select>
          <i class="bi bi-chevron-down select-arrow"></i>
        </div>
      </div>
    </div>

    <!-- Treks Grid -->
    <div class="row g-4 mb-5">
      <div v-for="trek in paginatedTreks" :key="trek.name" class="col-12 col-md-4">
        <div class="trek-browse-card">
          <div class="card-img-wrapper">
            <img :src="trek.image" :alt="trek.name" />
            <span class="difficulty-badge" :class="trek.difficulty.toLowerCase()">
              {{ trek.difficulty }}
            </span>
          </div>
          
          <div class="card-body-custom">
            <h4 class="trek-title-large">{{ trek.name }}</h4>
            
            <div class="trek-spec-list">
              <div class="spec-row">
                <span class="spec-label">Location</span>
                <span class="spec-value">{{ trek.location }}</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Difficulty</span>
                <span class="spec-value">{{ trek.difficulty }}</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Duration</span>
                <span class="spec-value">{{ trek.duration }}</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Slots Left</span>
                <span class="spec-value" :class="{ 'slots-empty': trek.slots === 0 }">
                  {{ trek.slots }}
                </span>
              </div>
            </div>

            <div class="card-footer-action row g-2">
              <div class="col-6">
                <button class="btn btn-secondary-outline btn-sm w-100 py-2 text-xs" @click="$emit('view-details', trek.name)">
                  Details
                </button>
              </div>
              <div class="col-6">
                <button 
                  class="btn btn-sm w-100 py-2 text-xs" 
                  :class="getTrekBtnClass(trek)"
                  :disabled="trek.status === 'Closed' || trek.status === 'Completed' || trek.slots === 0 || getTrekBookingStatus(trek.id) !== null || hasClashingBooking(trek)"
                  @click="$emit('book-trek', trek.id)"
                >
                  {{ getTrekBtnText(trek) }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredTreks.length === 0" class="col-12 text-center py-5">
        <div class="empty-state-container">
          <span class="empty-state-icon">🔍</span>
          <h3>No treks match your search</h3>
          <p>Try resetting the difficulty/location dropdowns or type a different query.</p>
          <button class="btn btn-secondary-outline mt-3" @click="$emit('reset-filters')">Reset Filters</button>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="pagination-bar mb-4">
      <button 
        class="page-btn" 
        :disabled="currentPage === 1" 
        @click="$emit('update:currentPage', currentPage - 1)"
      >
        <i class="bi bi-chevron-left"></i>
      </button>
      
      <button 
        v-for="page in totalPages" 
        :key="page" 
        class="page-btn" 
        :class="{ active: currentPage === page }"
        @click="$emit('update:currentPage', page)"
      >
        {{ page }}
      </button>

      <button 
        class="page-btn" 
        :disabled="currentPage === totalPages" 
        @click="$emit('update:currentPage', currentPage + 1)"
      >
        <i class="bi bi-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  searchQuery: {
    type: String,
    required: true
  },
  difficultyFilter: {
    type: String,
    required: true
  },
  locationFilter: {
    type: String,
    required: true
  },
  currentPage: {
    type: Number,
    required: true
  },
  paginatedTreks: {
    type: Array,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  filteredTreks: {
    type: Array,
    required: true
  },
  myBookingsList: {
    type: Array,
    required: true
  }
})

defineEmits([
  'update:searchQuery',
  'update:difficultyFilter',
  'update:locationFilter',
  'update:currentPage',
  'reset-filters',
  'view-details',
  'book-trek'
])

const getTrekBookingStatus = (trekId) => {
  if (!props.myBookingsList) return null
  const booking = props.myBookingsList.find(b => b.trekId === trekId && b.status !== 'Cancelled')
  return booking ? booking.status : null
}

const hasClashingBooking = (trek) => {
  if (!props.myBookingsList) return false
  return props.myBookingsList.some(b => b.startDate === trek.start_date && b.status !== 'Cancelled' && b.trekId !== trek.id)
}

const getTrekBtnText = (trek) => {
  if (trek.status === 'Closed') return 'Closed'
  if (trek.status === 'Completed') return 'Completed'
  const status = getTrekBookingStatus(trek.id)
  if (status === 'Pending') return 'Pending'
  if (status === 'Confirmed' || status === 'Booked') return 'Booked'
  if (hasClashingBooking(trek)) return 'Date Clash'
  return trek.slots > 0 ? 'Book Now' : 'Full'
}

const getTrekBtnClass = (trek) => {
  if (trek.status === 'Closed' || trek.status === 'Completed') return 'btn-disabled bg-secondary text-white border-0'
  const status = getTrekBookingStatus(trek.id)
  if (status === 'Pending') return 'btn-disabled bg-warning text-dark border-0'
  if (status === 'Confirmed' || status === 'Booked') return 'btn-disabled bg-success text-white border-0'
  if (hasClashingBooking(trek)) return 'btn-disabled bg-danger text-white border-0'
  return trek.slots > 0 ? 'btn-primary-accent' : 'btn-disabled'
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Browse Treks View Specific Styles */
.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-input-wrapper {
  position: relative;
  flex-grow: 1;
  max-width: 480px;
}

.search-icon {
  position: absolute;
  left: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-secondary);
  font-size: 0.95rem;
}

.search-control {
  width: 100%;
  padding: 0.65rem 1rem 0.65rem 2.5rem;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  font-size: 0.9rem;
  color: var(--color-text-primary);
  background-color: var(--color-card);
  outline: none;
  transition: all 0.2s ease;
}

.search-control:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.filter-dropdowns {
  display: flex;
  gap: 0.75rem;
}

.select-wrapper {
  position: relative;
  min-width: 160px;
}

.select-control {
  width: 100%;
  padding: 0.65rem 2.25rem 0.65rem 1rem;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-text-primary);
  background-color: var(--color-card);
  appearance: none;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.select-control:focus {
  border-color: var(--color-accent);
}

.select-arrow {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  pointer-events: none;
}

/* Trek Browse Card list */
.trek-browse-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.trek-browse-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.03);
}

.card-img-wrapper {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
  overflow: hidden;
}

.card-img-wrapper img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.difficulty-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
}

.difficulty-badge.easy {
  background-color: #E6FDF4;
  color: #10B981;
}

.difficulty-badge.moderate {
  background-color: #EFF6FF;
  color: #3B82F6;
}

.difficulty-badge.hard, .difficulty-badge.difficult {
  background-color: #FEF2F2;
  color: #EF4444;
}

.card-body-custom {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.trek-title-large {
  font-size: 1.2rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  letter-spacing: -0.02em;
}

.trek-spec-list {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.spec-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.spec-label {
  color: var(--color-text-secondary);
  font-weight: 500;
}

.spec-value {
  color: var(--color-text-primary);
  font-weight: 600;
}

.slots-empty {
  color: #EF4444;
  font-weight: 700;
}

.card-footer-action {
  margin-top: 1.5rem;
}

.btn-primary-accent {
  background-color: var(--color-accent);
  color: #FFFFFF;
  border: none;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  transition: opacity 0.2s ease;
}

.btn-primary-accent:hover {
  opacity: 0.9;
  color: #FFFFFF;
}

.btn-disabled {
  background-color: #F3F4F6;
  border: 1px solid var(--color-border);
  color: #9CA3AF;
  cursor: not-allowed;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
}

/* Empty State Styling */
.empty-state-container {
  padding: 3rem 1.5rem;
  background-color: var(--color-card);
  border: 1px dashed var(--color-border);
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-state-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.empty-state-container h3 {
  font-size: 1.15rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.empty-state-container p {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-bottom: 0;
}

.btn-secondary-outline {
  background-color: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.btn-secondary-outline:hover {
  background-color: var(--color-bg);
  color: var(--color-text-primary);
  border-color: #D1D1D1;
}

/* Paginator */
.pagination-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.page-btn {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  background-color: var(--color-bg);
  color: var(--color-text-primary);
  border-color: #D1D1D1;
}

.page-btn.active {
  background-color: var(--color-accent-light);
  color: var(--color-accent);
  border-color: var(--color-accent);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
