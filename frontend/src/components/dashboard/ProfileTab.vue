<template>
  <div class="dashboard-container">
    <div class="profile-card">
      <div class="profile-card-header">
        <h3>Manage Account</h3>
        <p>Update your personal information and password.</p>
      </div>
      
      <div class="profile-card-body">
        <div v-if="profileError" class="feedback-banner error-banner mb-4 animate-fade-in">
          <i class="bi bi-exclamation-circle-fill"></i>
          <span>{{ profileError }}</span>
        </div>
        <div v-if="profileSuccess" class="feedback-banner success-banner mb-4 animate-fade-in">
          <i class="bi bi-check-circle-fill"></i>
          <span>{{ profileSuccess }}</span>
        </div>

        <div class="row g-4">
          <!-- Details Form Column -->
          <div class="col-12">
            <form @submit.prevent="handleSubmit" class="profile-form d-flex flex-column gap-3">
              <div class="row g-3">
                <div class="col-12 col-md-6">
                  <label class="form-label-custom">Full Name</label>
                  <input v-model="localName" type="text" placeholder="Your Name" class="form-control-custom" required />
                </div>
                <div class="col-12 col-md-6">
                  <label class="form-label-custom">Email Address</label>
                  <input v-model="localEmail" type="email" placeholder="email@example.com" class="form-control-custom" required />
                </div>
              </div>

              <div class="row g-3">
                <div class="col-12 col-md-6">
                  <label class="form-label-custom">Phone Number</label>
                  <input v-model="localPhone" type="tel" placeholder="Phone Number" class="form-control-custom" required />
                </div>
                <div class="col-12 col-md-6">
                  <label class="form-label-custom">New Password</label>
                  <input v-model="localPassword" type="password" placeholder="•••••••• (leave blank to keep current)" class="form-control-custom" />
                </div>
              </div>

              <div class="form-actions mt-4">
                <button type="submit" class="btn btn-primary-accent px-4 py-2" :disabled="isSavingProfile">
                  <span v-if="isSavingProfile" class="spinner-border spinner-border-sm me-2"></span>
                  Save Changes
                </button>
                <button type="button" class="btn btn-secondary-outline px-4 py-2" @click="$emit('cancel')">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  profileName: {
    type: String,
    required: true
  },
  profileEmail: {
    type: String,
    required: true
  },
  profilePhone: {
    type: String,
    required: true
  },
  profilePassword: {
    type: String,
    required: true
  },
  isSavingProfile: {
    type: Boolean,
    required: true
  },
  profileError: {
    type: String,
    required: true
  },
  profileSuccess: {
    type: String,
    required: true
  },
  customAvatarInput: {
    type: String,
    required: true
  },
  avatarUrl: {
    type: String,
    required: true
  },
  avatarPresets: {
    type: Array,
    required: true
  }
})

const emit = defineEmits([
  'update:customAvatarInput',
  'update:profileName',
  'update:profileEmail',
  'update:profilePhone',
  'update:profilePassword',
  'save-profile',
  'save-avatar',
  'cancel'
])

const localName = ref(props.profileName)
const localEmail = ref(props.profileEmail)
const localPhone = ref(props.profilePhone)
const localPassword = ref(props.profilePassword)

watch(() => props.profileName, (val) => localName.value = val)
watch(() => props.profileEmail, (val) => localEmail.value = val)
watch(() => props.profilePhone, (val) => localPhone.value = val)
watch(() => props.profilePassword, (val) => localPassword.value = val)

const handleSubmit = () => {
  emit('update:profileName', localName.value)
  emit('update:profileEmail', localEmail.value)
  emit('update:profilePhone', localPhone.value)
  emit('update:profilePassword', localPassword.value)
  emit('save-profile')
}
</script>

<style scoped>
.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Profile Card Styles */
.profile-card {
  background-color: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  overflow: hidden;
  margin-top: 1rem;
}

.profile-card-header {
  padding: 1.75rem;
  border-bottom: 1px solid var(--color-border);
}

.profile-card-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.profile-card-header p {
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  margin-bottom: 0;
}

.profile-card-body {
  padding: 1.75rem;
}

.border-end-custom {
  border-right: 1px solid var(--color-border);
}

@media (max-width: 767.98px) {
  .border-end-custom {
    border-right: none;
    border-bottom: 1px solid var(--color-border);
    padding-bottom: 2rem;
    margin-bottom: 2rem;
  }
}

.avatar-preview-wrapper {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto;
  border: 3px solid var(--color-card);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.avatar-large {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-title {
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.avatar-subtitle {
  color: var(--color-text-secondary);
  font-size: 0.75rem;
  margin-bottom: 1.25rem;
}

.avatar-options {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.avatar-option-thumb {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s ease;
  object-fit: cover;
}

.avatar-option-thumb:hover {
  transform: scale(1.1);
}

.avatar-option-thumb.active {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 2px var(--color-accent-light);
}

.custom-avatar-url {
  margin-top: 1rem;
}

.form-label-custom {
  font-size: 0.75rem;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
  display: block;
}

.form-control-custom {
  width: 100%;
  padding: 0.65rem 1rem;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  font-size: 0.9rem;
  color: var(--color-text-primary);
  background-color: var(--color-card);
  outline: none;
  transition: all 0.2s ease;
}

.form-control-custom:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  border-top: 1px solid var(--color-border);
  padding-top: 1.5rem;
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

/* Feedback banners (sometimes in global but adding just in case) */
.feedback-banner {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 500;
}

.error-banner {
  background-color: #FEF2F2;
  color: #EF4444;
  border: 1px solid #FCA5A5;
}

.success-banner {
  background-color: #E6FDF4;
  color: #10B981;
  border: 1px solid #A7F3D0;
}
</style>
