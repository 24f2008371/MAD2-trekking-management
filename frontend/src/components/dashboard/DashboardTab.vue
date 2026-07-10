<template>
  <div class="dashboard-container">
    <!-- 12-Column Grid -->
    <div class="row g-4">
      <!-- Section 2 — Available Treks -->
      <div class="col-12 mt-5">
        <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-3">
          <h2 class="section-title mb-0">Available Treks</h2>
          
          <!-- Filter Dropdowns for Dashboard -->
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

        <!-- Treks Row -->
        <div class="row g-4">
          <div v-for="trek in dashboardFilteredTreks" :key="trek.name" class="col-12 col-md-4">
            <div class="trek-browse-card">
              <div class="card-img-wrapper">
                <img :src="trek.image" :alt="trek.name" />
                <span class="difficulty-badge" :class="trek.difficulty.toLowerCase()">
                  {{ trek.difficulty }}
                </span>
              </div>
              
              <div class="card-body-custom d-flex flex-column h-100">
                <h4 class="trek-title-large mb-2">{{ trek.name }}</h4>
                
                <div class="trek-spec-list mb-3">
                  <div class="spec-text-single">{{ trek.location }}</div>
                  <div class="spec-text-single text-muted">{{ trek.difficulty }} - {{ trek.duration }}</div>
                  <div class="spec-text-single mt-1">
                    Slots Left: <span :class="{ 'text-danger fw-bold': trek.slots === 0 }">{{ trek.slots }}</span>
                  </div>
                </div>                 <div class="card-footer-action mt-auto">
                  <button 
                    class="btn w-100" 
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
          
          <!-- Empty State for Dashboard filters -->
          <div v-if="dashboardFilteredTreks.length === 0" class="col-12 text-center py-4">
            <div class="empty-state-container py-4">
              <span class="empty-state-icon">🔍</span>
              <h3>No treks match filters</h3>
              <p>Try resetting filters or checking the Browse Treks tab.</p>
            </div>
          </div>
        </div>
        
        <!-- Show More Link for Available Treks -->
        <div class="d-flex justify-content-end mt-3" v-if="dashboardFilteredTreks.length > 0">
          <a href="#" class="view-all-link text-decoration-none" @click.prevent="$emit('change-tab', 'explore')">
            Show More Treks <i class="bi bi-arrow-right ms-1"></i>
          </a>
        </div>
      </div>

      <!-- Section 3 — My Bookings -->
      <div class="col-12 mt-5 mb-3">
        <h2 class="section-title mb-4">My Bookings</h2>
        <div class="bookings-table-card">
          <div v-if="myBookingsList.length === 0" class="text-center py-4 text-secondary">
            <p class="mb-0">You don't have any bookings yet. Book a trek to see it here!</p>
          </div>
          <div v-else class="table-responsive">
            <table class="table table-custom align-middle">
              <thead>
                <tr>
                  <th>Trek Name</th>
                  <th>Booking Date</th>
                  <th>Trek Dates</th>
                  <th>Status</th>
                  <th class="text-end">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="booking in myBookingsList.slice(0, 3)" :key="booking.id">
                  <td class="fw-bold text-dark">{{ booking.trekName }}</td>
                  <td class="text-secondary">{{ booking.bookingDate }}</td>
                  <td class="text-secondary">{{ booking.trekDates }}</td>
                  <td>
                    <span :class="getStatusClass(booking.status)">
                      {{ booking.status }}
                    </span>
                  </td>
                  <td class="text-end">
                    <button class="btn btn-secondary-outline btn-sm px-3" @click="$emit('view-details', booking.trekName)">
                      View Details
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="d-flex justify-content-end mt-3">
            <a href="#" class="view-all-link text-decoration-none" @click.prevent="$emit('change-tab', 'bookings')">
              View All Bookings <i class="bi bi-arrow-right ms-1"></i>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  dashboardFilteredTreks: {
    type: Array,
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
  myBookingsList: {
    type: Array,
    required: true
  }
})

defineEmits(['update:difficultyFilter', 'update:locationFilter', 'view-details', 'change-tab', 'book-trek'])

const getStatusClass = (status) => {
  if (status === 'Pending') return 'status-badge-orange'
  if (status === 'Cancelled') return 'status-badge-red'
  if (status === 'Confirmed' || status === 'Booked') return 'status-badge-green'
  return 'status-badge-blue'
}

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

.section-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 1.5rem;
  letter-spacing: -0.01em;
}

/* Stat Cards */
.stat-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.02);
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-icon {
  font-size: 1.25rem;
  background-color: #FBFBFA;
  border: 1px solid var(--color-border);
  width: 38px;
  height: 38px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
}

.stat-trend {
  font-size: 0.725rem;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 20px;
}

.stat-trend.positive {
  background-color: #E6FDF4;
  color: #10B981;
}

.stat-trend.neutral {
  background-color: #F3F4F6;
  color: #4B5563;
}

.stat-trend.premium {
  background-color: #FFFBEB;
  color: #D97706;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.03em;
  margin-bottom: 0.15rem;
}

.stat-title {
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  margin: 0;
}

/* Available Treks Filters */
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

/* Trek Cards */
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

.spec-text-single {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-text-primary);
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

/* Empty State */
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

/* Bookings Table */
.bookings-table-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 1.5rem;
}

.table-custom {
  margin-bottom: 0;
  width: 100%;
}

.table-custom th {
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.05em;
  padding: 1rem 0.75rem;
}

.table-custom td {
  padding: 1.25rem 0.75rem;
  border-bottom: 1px solid var(--color-border);
  font-size: 0.9rem;
}

.status-badge-blue {
  background-color: #EFF6FF;
  color: #3B82F6;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
}

.status-badge-green {
  background-color: #E6FDF4;
  color: #10B981;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
}

.status-badge-orange {
  background-color: #FFF3CD;
  color: #856404;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
}

.status-badge-red {
  background-color: #F8D7DA;
  color: #721C24;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
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

.view-all-link {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--color-accent);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  transition: gap 0.2s ease;
}

.view-all-link:hover {
  gap: 0.5rem;
}
</style>
