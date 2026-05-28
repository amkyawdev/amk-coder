import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'

// Register service worker for PWA
if ('serviceWorker' in navigator) {
  import('virtual:pwa-register').then(({ registerSW }) => {
    registerSW({
      onNeedRefresh() {
        // Show update notification
        if (confirm('New version available. Reload?')) {
          window.location.reload()
        }
      },
      onOfflineReady() {
        console.log('App ready to work offline')
      }
    })
  }).catch(() => {
    // PWA plugin not available in dev mode
  })
}

const app = createApp(App)
app.use(router)
app.mount('#app')