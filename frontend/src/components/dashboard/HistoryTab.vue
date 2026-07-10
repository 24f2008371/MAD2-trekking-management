<template>
  <div class="dashboard-container">
    <div class="bookings-table-card">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h3 class="mb-0">Trekking History</h3>
        <span class="badge bg-light text-dark border">{{ historyList.length }} Completed Treks</span>
      </div>

      <div v-if="historyList.length === 0" class="text-center py-5">
        <span class="fs-1 d-block mb-3">🥾</span>
        <h4 class="text-muted">No completed treks found</h4>
        <p class="text-secondary text-sm mb-0">Your completed expeditions will appear here once the trek duration finishes!</p>
      </div>
      
      <div v-else class="table-responsive">
        <table class="table table-custom align-middle">
          <thead>
            <tr>
              <th>Trek Name</th>
              <th>Trek Dates</th>
              <th>Completed On</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trek in historyList" :key="trek.id || trek.trekName">
              <td class="fw-bold text-dark">{{ trek.trekName }}</td>
              <td class="text-secondary">{{ trek.trekDates }}</td>
              <td class="text-secondary">{{ trek.completedOn || 'N/A' }}</td>
              <td>
                <span class="status-badge-green">
                  {{ trek.status }}
                </span>
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
  historyList: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* History Table Styles */
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

.table-custom tr:last-child td {
  border-bottom: none;
}

.status-badge-green {
  background-color: #E6FDF4;
  color: #10B981;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
}
</style>
