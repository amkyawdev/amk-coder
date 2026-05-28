<template>
  <div class="min-h-[calc(100vh-8rem)] flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <!-- Glassmorphic Card -->
      <div class="glass rounded-3xl p-8 shadow-glass">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-cyber-accent to-cyber-accent-light flex items-center justify-center mx-auto mb-4">
            <span class="text-3xl font-bold text-white font-mono">⟨⟩</span>
          </div>
          <h1 class="text-2xl font-bold text-white mb-2">Welcome to AMK AI</h1>
          <p class="text-gray-400">Sign in to unlock advanced AI capabilities</p>
        </div>

        <!-- Tab Switcher -->
        <div class="flex rounded-xl bg-cyber-surface p-1 mb-6">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'flex-1 py-2.5 rounded-lg font-medium text-sm transition-all duration-200',
              activeTab === tab.id
                ? 'bg-cyber-accent text-white shadow-glow'
                : 'text-gray-400 hover:text-white'
            ]"
          >
            {{ tab.label }}
          </button>
        </div>

        <!-- Login Form -->
        <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="space-y-4">
          <Input
            v-model="loginForm.email"
            type="email"
            label="Email"
            placeholder="you@example.com"
            :error="errors.email"
            autocomplete="email"
          />
          <Input
            v-model="loginForm.password"
            type="password"
            label="Password"
            placeholder="••••••••"
            :error="errors.password"
            autocomplete="current-password"
          />
          <Button
            type="submit"
            variant="primary"
            size="lg"
            :loading="loading"
            class="w-full"
          >
            Sign In
          </Button>
        </form>

        <!-- Register Form -->
        <form v-else @submit.prevent="handleRegister" class="space-y-4">
          <Input
            v-model="registerForm.email"
            type="email"
            label="Email"
            placeholder="you@example.com"
            :error="errors.email"
            autocomplete="email"
          />
          <Input
            v-model="registerForm.password"
            type="password"
            label="Password"
            placeholder="Min 6 characters"
            :error="errors.password"
            autocomplete="new-password"
          />
          <Input
            v-model="registerForm.confirmPassword"
            type="password"
            label="Confirm Password"
            placeholder="••••••••"
            :error="errors.confirmPassword"
            autocomplete="new-password"
          />
          <Button
            type="submit"
            variant="primary"
            size="lg"
            :loading="loading"
            class="w-full"
          >
            Create Account
          </Button>
        </form>

        <!-- Divider -->
        <div class="flex items-center gap-4 my-6">
          <div class="flex-1 h-px bg-cyber-border" />
          <span class="text-sm text-gray-400">or</span>
          <div class="flex-1 h-px bg-cyber-border" />
        </div>

        <!-- Social Login -->
        <Button
          variant="secondary"
          size="lg"
          :loading="googleLoading"
          @click="handleGoogleSignIn"
          class="w-full"
        >
          <svg class="w-5 h-5" viewBox="0 0 24 24">
            <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          Continue with Google
        </Button>

        <!-- Error Alert -->
        <div
          v-if="authError"
          class="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm"
        >
          {{ authError }}
        </div>
      </div>

      <!-- Footer -->
      <p class="text-center text-sm text-gray-500 mt-6">
        By continuing, you agree to our
        <a href="#" class="text-cyber-accent hover:underline">Terms of Service</a>
        and
        <a href="#" class="text-cyber-accent hover:underline">Privacy Policy</a>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@/composables/useAuth'
import Button from '@/components/ui/Button.vue'
import Input from '@/components/ui/Input.vue'

const router = useRouter()
const route = useRoute()
const { signIn, signUp, signInWithGoogle, error: authError } = useAuth()

const tabs = [
  { id: 'login', label: 'Sign In' },
  { id: 'register', label: 'Register' }
]

const activeTab = ref('login')
const loading = ref(false)
const googleLoading = ref(false)

const loginForm = reactive({
  email: '',
  password: ''
})

const registerForm = reactive({
  email: '',
  password: '',
  confirmPassword: ''
})

const errors = reactive({
  email: '',
  password: '',
  confirmPassword: ''
})

const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

const validateForm = (isRegister = false) => {
  let valid = true
  errors.email = ''
  errors.password = ''
  errors.confirmPassword = ''

  const form = isRegister ? registerForm : loginForm

  if (!form.email) {
    errors.email = 'Email is required'
    valid = false
  } else if (!validateEmail(form.email)) {
    errors.email = 'Please enter a valid email'
    valid = false
  }

  if (!form.password) {
    errors.password = 'Password is required'
    valid = false
  } else if (isRegister && form.password.length < 6) {
    errors.password = 'Password must be at least 6 characters'
    valid = false
  }

  if (isRegister && form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
    valid = false
  }

  return valid
}

const handleLogin = async () => {
  if (!validateForm(false)) return

  loading.value = true
  try {
    await signIn(loginForm.email, loginForm.password)
    const redirect = route.query.redirect || '/chat'
    router.push(redirect)
  } catch (err) {
    // Error handled by composable
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (!validateForm(true)) return

  loading.value = true
  try {
    await signUp(registerForm.email, registerForm.password)
    const redirect = route.query.redirect || '/chat'
    router.push(redirect)
  } catch (err) {
    // Error handled by composable
  } finally {
    loading.value = false
  }
}

const handleGoogleSignIn = async () => {
  googleLoading.value = true
  try {
    await signInWithGoogle()
    const redirect = route.query.redirect || '/chat'
    router.push(redirect)
  } catch (err) {
    // Error handled by composable
  } finally {
    googleLoading.value = false
  }
}
</script>