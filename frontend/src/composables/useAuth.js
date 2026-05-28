import { ref, computed } from 'vue'
import { initializeApp } from 'firebase/app'
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  signOut,
  onAuthStateChanged
} from 'firebase/auth'

// Firebase configuration - replace with your own config
const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || '',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || '',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || '',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || '',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || ''
}

const app = initializeApp(firebaseConfig)
const auth = getAuth(app)
const googleProvider = new GoogleAuthProvider()

const user = ref(null)
const loading = ref(true)
const error = ref(null)

// Initialize auth state listener
onAuthStateChanged(auth, (firebaseUser) => {
  user.value = firebaseUser
  loading.value = false
})

export function useAuth() {
  const isAuthenticated = computed(() => !!user.value)

  const signIn = async (email, password) => {
    error.value = null
    loading.value = true
    try {
      const result = await signInWithEmailAndPassword(auth, email, password)
      user.value = result.user
      return result.user
    } catch (err) {
      error.value = getErrorMessage(err.code)
      throw err
    } finally {
      loading.value = false
    }
  }

  const signUp = async (email, password) => {
    error.value = null
    loading.value = true
    try {
      const result = await createUserWithEmailAndPassword(auth, email, password)
      user.value = result.user
      return result.user
    } catch (err) {
      error.value = getErrorMessage(err.code)
      throw err
    } finally {
      loading.value = false
    }
  }

  const signInWithGoogle = async () => {
    error.value = null
    loading.value = true
    try {
      const result = await signInWithPopup(auth, googleProvider)
      user.value = result.user
      return result.user
    } catch (err) {
      error.value = getErrorMessage(err.code)
      throw err
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    error.value = null
    try {
      await signOut(auth)
      user.value = null
    } catch (err) {
      error.value = getErrorMessage(err.code)
      throw err
    }
  }

  const getIdToken = async () => {
    if (user.value) {
      return await user.value.getIdToken()
    }
    return null
  }

  return {
    user,
    loading,
    error,
    isAuthenticated,
    signIn,
    signUp,
    signInWithGoogle,
    logout,
    getIdToken
  }
}

function getErrorMessage(code) {
  const messages = {
    'auth/email-already-in-use': 'This email is already registered',
    'auth/invalid-email': 'Please enter a valid email address',
    'auth/operation-not-allowed': 'This sign-in method is not enabled',
    'auth/weak-password': 'Password should be at least 6 characters',
    'auth/user-disabled': 'This account has been disabled',
    'auth/user-not-found': 'No account found with this email',
    'auth/wrong-password': 'Incorrect password',
    'auth/too-many-requests': 'Too many failed attempts. Please try again later',
    'auth/popup-closed-by-user': 'Sign-in was cancelled'
  }
  return messages[code] || 'An authentication error occurred'
}