import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '@/composables/useAuth'

const routes = [
  {
    path: '/',
    name: 'get-started',
    component: () => import('@/views/GetStarted.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import('@/views/Auth.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/chat',
    name: 'chat',
    component: () => import('@/views/Chat.vue'),
    meta: { requiresAuth: false }  // Temporarily disabled for testing
  },
  {
    path: '/api-keys',
    name: 'api-keys',
    component: () => import('@/views/ApiKeyInput.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/docs',
    name: 'docs',
    component: () => import('@/views/Docs.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/About.vue'),
    meta: { requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const { isAuthenticated, loading } = useAuth()

  // Skip auth check during loading
  if (loading.value) {
    next()
    return
  }

  // Check if route requires auth
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next({ name: 'auth', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router