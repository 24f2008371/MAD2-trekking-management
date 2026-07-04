<template>
  <div class="form-container">
    <!-- Header -->
    <div class="text-center mb-4">
      <h3 class="form-title font-heading mb-1 text-dark">Create Account</h3>
      <p class="form-subtitle text-muted text-sm">Start your trekking journey today.</p>
    </div>

    <!-- Feedback Banners -->
    <div v-if="errorMsg" class="feedback-banner error-banner mb-3 animate-fade-in">
      <i class="bi bi-exclamation-circle-fill"></i>
      <span>{{ errorMsg }}</span>
    </div>
    <div v-if="successMsg" class="feedback-banner success-banner mb-3 animate-fade-in">
      <i class="bi bi-check-circle-fill"></i>
      <span>{{ successMsg }}</span>
    </div>

    <!-- Inputs Form -->
    <form @submit.prevent="handleRegister" novalidate class="d-flex flex-column gap-3">

      <!-- Grid Row 1 -->
      <div class="row g-3">
        <!-- Full Name -->
        <div class="col-6 form-group position-relative">
          <label class="input-label">Full Name</label>
          <div class="input-wrapper" :class="{ 'error-state': nameErr }">
            <i class="bi bi-person input-icon"></i>
            <input v-model="name" type="text" placeholder="John Doe" class="light-input" @blur="validateName"
              @input="clearErrors" />
          </div>
          <div v-if="nameErr" class="error-msg-text">
            <i class="bi bi-info-circle"></i> {{ nameErr }}
          </div>
        </div>

        <!-- Email -->
        <div class="col-6 form-group position-relative">
          <label class="input-label">Email Address</label>
          <div class="input-wrapper" :class="{ 'error-state': emailErr }">
            <i class="bi bi-envelope input-icon"></i>
            <input v-model="email" type="email" placeholder="name@example.com" class="light-input" @blur="validateEmail"
              @input="clearErrors" />
          </div>
          <div v-if="emailErr" class="error-msg-text">
            <i class="bi bi-info-circle"></i> {{ emailErr }}
          </div>
        </div>
      </div>

      <!-- Grid Row 2 -->
      <div class="row g-3">
        <!-- Phone Number -->
        <div class="col-6 form-group position-relative">
          <label class="input-label">Phone Number</label>
          <div class="input-wrapper" :class="{ 'error-state': phoneErr }">
            <i class="bi bi-telephone input-icon"></i>
            <input v-model="phone" type="tel" placeholder="+1 (555) 000-0000" class="light-input" @blur="validatePhone"
              @input="clearErrors" />
          </div>
          <div v-if="phoneErr" class="error-msg-text">
            <i class="bi bi-info-circle"></i> {{ phoneErr }}
          </div>
        </div>

        <!-- Password -->
        <div class="col-6 form-group position-relative">
          <label class="input-label">Password</label>
          <div class="input-wrapper" :class="{ 'error-state': pwdErr }">
            <i class="bi bi-lock input-icon"></i>
            <input v-model="password" :type="showPassword ? 'text' : 'password'" placeholder="••••••••"
              class="light-input pe-5" @blur="validatePassword" @input="clearErrors" />
            <button type="button" class="btn-eye-toggle" @click="showPassword = !showPassword">
              <i class="bi" :class="showPassword ? 'bi-eye-slash' : 'bi-eye'"></i>
            </button>
          </div>
          <div v-if="pwdErr" class="error-msg-text">
            <i class="bi bi-info-circle"></i> {{ pwdErr }}
          </div>
        </div>
      </div>

      <!-- Terms & Policies -->
      <div class="mt-1">
        <label class="custom-check-container align-items-start text-start">
          <input v-model="agreeToTerms" type="checkbox" class="check-box-input" />
          <span class="checkmark mt-1"></span>
          <span class="check-label text-muted text-sm ms-2">
            I agree to the <a href="#" @click.prevent class="terms-link text-decoration-none">Terms & Privacy Policy</a>
          </span>
        </label>
        <div v-if="termsErr" class="error-msg-text text-start">
          <i class="bi bi-info-circle"></i> {{ termsErr }}
        </div>
      </div>

      <!-- Submit Button -->
      <button type="submit" class="btn-gradient-orange mt-2" :disabled="isSubmitting">
        <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
        <span>Create Account</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api/api.js'

const emit = defineEmits(['auth-success'])

// Form States
const name = ref('')
const email = ref('')
const phone = ref('')
const password = ref('')
const agreeToTerms = ref(false)

const showPassword = ref(false)

const isSubmitting = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

// Field Errors
const nameErr = ref('')
const emailErr = ref('')
const phoneErr = ref('')
const pwdErr = ref('')
const termsErr = ref('')

const validateName = () => {
  if (!name.value.trim()) {
    nameErr.value = 'Full name is required'
    return false
  }
  nameErr.value = ''
  return true
}

const validateEmail = () => {
  if (!email.value) {
    emailErr.value = 'Email address is required'
    return false
  }
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!regex.test(email.value)) {
    emailErr.value = 'Please enter a valid email'
    return false
  }
  emailErr.value = ''
  return true
}

const validatePhone = () => {

  if (!phone.value) {
    phoneErr.value = 'Phone number is required'
    return false
  }

  const digits = phone.value.replace(/[\s()+-]/g, '')

  if (digits.length < 1) {
    phoneErr.value = 'Phone number is required'
    return false
  }

  phoneErr.value = ''
  return true
}

const validatePassword = () => {
  if (!password.value) {
    pwdErr.value = 'Password is required'
    return false
  }

  pwdErr.value = ''
  return true
}

const clearErrors = () => {
  errorMsg.value = ''
  successMsg.value = ''
  termsErr.value = ''
}

const handleRegister = async () => {
  clearErrors()

  const isNameVal = validateName()
  const isEmailVal = validateEmail()
  const isPhoneVal = validatePhone()
  const isPwdVal = validatePassword()

  if (!agreeToTerms.value) {
    termsErr.value = 'You must agree to the terms.'
  }

  if (!isNameVal || !isEmailVal || !isPhoneVal || !isPwdVal || !agreeToTerms.value) {
    errorMsg.value = 'Please fill all fields correctly.'
    return
  }

  // isSubmitting.value = true
  // setTimeout(() => {
  //   isSubmitting.value = false
  //   successMsg.value = 'Registration successful! Directing to Login...'
  //   setTimeout(() => {
  //     emit('auth-success')
  //   }, 1500)
  // }, 1500)

  isSubmitting.value = true

  try {

    const response = await api.post("/register", {

      username: name.value,
      email: email.value,
      phone: phone.value,
      password: password.value

    })

    successMsg.value = response.data.message

    setTimeout(() => {
      emit("auth-success")
    }, 1500)

  }

  catch (error) {

    if (error.response) {

      errorMsg.value = error.response.data.message

    }

    else {

      errorMsg.value = "Server not reachable."

    }

  }

  finally {

    isSubmitting.value = false

  }
}
</script>

<style scoped>
.form-title {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.text-sm {
  font-size: 0.85rem;
}

/* Light inputs styling */
.form-group {
  text-align: left;
}

.input-label {
  font-size: 0.725rem;
  text-transform: uppercase;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #6B7280;
  margin-bottom: 6px;
  display: block;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  background: #F8FAFC;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.input-wrapper:focus-within {
  border-color: var(--accent-orange);
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(255, 107, 53, 0.12),
    0 2px 4px rgba(15, 23, 42, 0.02);
}

.input-wrapper.error-state {
  border-color: #EF4444;
}

.input-wrapper.error-state:focus-within {
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.12);
}

.input-icon {
  position: absolute;
  left: 16px;
  color: #94A3B8;
  font-size: 1.1rem;
  pointer-events: none;
}

.light-input {
  flex: 1;
  width: 100%;
  padding: 13px 16px 13px 48px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 0.95rem;
  color: #111827;
  border-radius: 16px;
}

.light-input::placeholder {
  color: #94A3B8;
}

.btn-eye-toggle {
  position: absolute;
  right: 16px;
  background: none;
  border: none;
  color: #94A3B8;
  padding: 0;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: color 0.2s ease;
}

.btn-eye-toggle:hover {
  color: var(--accent-orange);
}

/* Custom Checkbox Design */
.custom-check-container {
  display: inline-flex;
  align-items: center;
  cursor: pointer;
  position: relative;
  user-select: none;
}

.check-box-input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  height: 18px;
  width: 18px;
  background-color: #ffffff;
  border: 1px solid #CBD5E1;
  border-radius: 6px;
  display: inline-block;
  transition: all 0.2s ease;
  position: relative;
  flex-shrink: 0;
}

.custom-check-container:hover .checkmark {
  border-color: #94A3B8;
}

.check-box-input:checked~.checkmark {
  background-color: var(--accent-orange);
  border-color: var(--accent-orange);
}

.checkmark::after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.check-box-input:checked~.checkmark::after {
  display: block;
}

/* Terms Link */
.terms-link {
  color: var(--accent-orange);
  font-weight: 500;
  transition: opacity 0.2s ease;
}

.terms-link:hover {
  opacity: 0.85;
}

/* Error messages */
.error-msg-text {
  color: #EF4444;
  font-size: 0.75rem;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Banner system */
.feedback-banner {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 0.825rem;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.error-banner {
  background: #FEF2F2;
  border: 1px solid #FCA5A5;
  color: #991B1B;
}

.success-banner {
  background: #F0FDF4;
  border: 1px solid #86EFAC;
  color: #166534;
}

/* Button style */
.btn-gradient-orange {
  background: var(--gradient-orange);
  color: white;
  font-weight: 600;
  border: none;
  padding: 13px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(255, 107, 53, 0.25);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-gradient-orange:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 53, 0.35);
}

.btn-gradient-orange:disabled {
  opacity: 0.7;
}
</style>
