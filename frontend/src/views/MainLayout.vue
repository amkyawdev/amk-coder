<template>
  <div class="min-h-screen bg-cyber-dark flex">
    <!-- Mobile Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="sidebarOpen"
        class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
        @click="closeSidebar"
      />
    </Transition>

    <!-- Sidebar -->
    <aside
      :class="[
        'fixed lg:static inset-y-0 left-0 z-50 w-72 bg-cyber-surface border-r border-cyber-border',
        'transform transition-transform duration-300 ease-out lg:translate-x-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      ]"
    >
      <!-- Logo -->
      <div class="h-16 flex items-center justify-between px-6 border-b border-cyber-border">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyber-accent to-cyber-accent-light flex items-center justify-center">
            <span class="text-xl font-bold text-white font-mono">⟨⟩</span>
          </div>
          <span class="text-lg font-semibold text-white">AMK AI</span>
        </div>
        <button
          @click="closeSidebar"
          class="lg:hidden p-2 rounded-lg text-gray-400 hover:text-white hover:bg-white/5"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 p-4 space-y-1">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200"
          :class="route.path === item.path
            ? 'bg-cyber-accent/10 text-cyber-accent border border-cyber-accent/20'
            : 'text-gray-400 hover:text-white hover:bg-white/5'"
          @click="closeSidebar"
        >
          <span v-html="item.icon" class="w-5 h-5 flex-shrink-0" />
          <span class="font-medium">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <!-- User Section -->
      <div class="p-4 border-t border-cyber-border">
        <div v-if="isAuthenticated" class="space-y-3">
          <div class="flex items-center gap-3 px-4 py-2">
            <div class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <span class="text-sm font-medium text-white">{{ userInitial }}</span>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-white truncate">{{ userEmail }}</p>
              <p class="text-xs text-gray-400">Signed in</p>
            </div>
          </div>
          <button
            @click="handleLogout"
            class="w-full flex items-center gap-3 px-4 py-2 rounded-xl text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span class="font-medium">Sign Out</span>
          </button>
        </div>
        <RouterLink
          v-else
          to="/auth"
          class="btn-primary w-full flex items-center justify-center gap-2"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Sign In
        </RouterLink>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-h-screen">
      <!-- Mobile Header -->
      <header class="lg:hidden h-16 flex items-center justify-between px-4 border-b border-cyber-border bg-cyber-surface/80 backdrop-blur-md sticky top-0 z-30">
        <button
          @click="openSidebar"
          class="p-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <div class="flex items-center gap-2">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-cyber-accent to-cyber-accent-light flex items-center justify-center">
            <span class="text-sm font-bold text-white font-mono">⟨⟩</span>
          </div>
          <span class="font-semibold text-white">AMK AI</span>
        </div>
        <div class="w-10" />
      </header>

      <!-- Page Content -->
      <main class="flex-1 p-4 lg:p-8">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink, RouterView, useRoute, useRouter } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const route = useRoute()
const router = useRouter()
const { user, isAuthenticated, logout } = useAuth()

const sidebarOpen = ref(false)

const navItems = [
  {
    label: 'Get Started',
    path: '/',
    icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>`
  },
  {
    label: 'Chat',
    path: '/chat',
    icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>`
  },
  {
    label: 'API Keys',
    path: '/api-keys',
    icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" /></svg>`
  },
  {
    label: 'Documentation',
    path: '/docs',
    icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>`
  },
  {
    label: 'About',
    path: '/about',
    icon: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`
  }
]

const userEmail = computed(() => user.value?.email || '')
const userInitial = computed(() => {
  const email = userEmail.value
  return email ? email[0].toUpperCase() : '?'
})

const openSidebar = () => {
  sidebarOpen.value = true
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

const handleLogout = async () => {
  try {
    await logout()
    router.push('/')
    closeSidebar()
  } catch (err) {
    console.error('Logout failed:', err)
  }
}
</script>