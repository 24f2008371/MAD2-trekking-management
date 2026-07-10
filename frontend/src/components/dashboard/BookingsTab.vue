<template>
  <div class="dashboard-container">
    <div class="bookings-table-card">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="mb-0">My Bookings</h3>
        <span class="badge bg-light text-dark border">{{ myBookingsList.length }} Bookings</span>
      </div>

      <div v-if="myBookingsList.length === 0" class="text-center py-5">
        <span class="fs-1 d-block mb-3">📅</span>
        <h4 class="text-muted">No bookings found</h4>
        <p class="text-secondary text-sm mb-0">You haven't booked any expeditions yet. Go to the Browse Treks section to book one!</p>
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
            <tr v-for="booking in myBookingsList" :key="booking.id || booking.trekName">
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
    </div>
  </div>
</template>

<script setup>
defineProps({
  myBookingsList: {
    type: Array,
    required: true
  }
})

defineEmits(['view-details'])

const getStatusClass = (status) => {
  if (status === 'Pending') return 'status-badge-orange'
  if (status === 'Cancelled') return 'status-badge-red'
  if (status === 'Confirmed' || status === 'Booked') return 'status-badge-green'
  return 'status-badge-blue'
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Bookings Table Styles */
.bookings-table-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  box-radius: 14px;
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

.table-custom tr:last-child td {
  border-bottom: none;
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
</style>
