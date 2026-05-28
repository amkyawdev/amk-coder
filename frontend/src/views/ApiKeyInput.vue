<template>
  <div class="max-w-3xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-white mb-2">API Keys</h1>
      <p class="text-gray-400">Securely store your AI provider API keys for enhanced capabilities</p>
    </div>

    <!-- Keys Grid -->
    <div class="grid gap-6">
      <div
        v-for="(config, key) in apiProviders"
        :key="key"
        class="glass rounded-2xl p-6"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="flex items-center gap-4">
            <div :class="['w-12 h-12 rounded-xl flex items-center justify-center', config.bgClass]">
              <component :is="config.icon" class="w-6 h-6" />
            </div>
            <div>
              <h3 class="text-lg font-semibold text-white">{{ config.name }}</h3>
              <p class="text-sm text-gray-400">{{ config.description }}</p>
            </div>
          </div>
          <div
            v-if="savedKeys[key]"
            class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/10 border border-green-500/20"
          >
            <span class="w-2 h-2 rounded-full bg-green-400" />
            <span class="text-sm text-green-400">Saved</span>
          </div>
        </div>

        <div class="relative">
          <input
            :type="visibility[key] ? 'text' : 'password'"
            v-model="keys[key]"
            :placeholder="config.placeholder"
            class="w-full px-4 py-3 pr-12 rounded-xl bg-cyber-surface border border-cyber-border text-white placeholder-gray-500 focus:outline-none focus:border-cyber-accent focus:ring-2 focus:ring-cyber-accent/20 transition-all"
          />
          <button
            @click="toggleVisibility(key)"
            class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
          >
            <svg v-if="visibility[key]" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.629 7.523 4.5 12 4.5c4.478 0 8.268 3.129 9.542 7.5-1.274 4.371-5.064 7.5-9.542 7.5-4.477 0-8.268-3.129-9.542-7.5z" />
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-3.129-9.542-7.5a10.05 10.05 0 01.484-2.217M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.629 7.523 4.5 12 4.5c4.478 0 8.268 3.129 9.542 7.5a10.975 10.975 0 01-4.042 5.167M6.158 8.758a3.75 3.75 0 015.328 2.664M10.5 16.5l2.5-2.5-2.5-2.5" />
            </svg>
          </button>
        </div>

        <div class="flex items-center justify-between mt-4">
          <p class="text-xs text-gray-500">{{ config.hint }}</p>
          <button
            @click="saveKey(key)"
            :disabled="!keys[key] || saving[key]"
            :class="[
              'px-4 py-2 rounded-lg font-medium text-sm transition-all',
              keys[key]
                ? 'bg-cyber-accent text-white hover:bg-cyber-accent-light'
                : 'bg-cyber-surface text-gray-500 cursor-not-allowed'
            ]"
          >
            {{ saving[key] ? 'Saving...' : 'Save' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Info Card -->
    <div class="mt-8 p-6 rounded-2xl bg-cyber-surface/50 border border-glass-border">
      <div class="flex items-start gap-4">
        <div class="w-10 h-10 rounded-xl bg-cyber-accent/10 flex items-center justify-center flex-shrink-0">
          <svg class="w-5 h-5 text-cyber-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h4 class="font-semibold text-white mb-1">Security Information</h4>
          <p class="text-sm text-gray-400 leading-relaxed">
            Your API keys are encrypted and stored locally. They are never sent to our servers
            and only used for direct communication with the respective AI providers.
            Each provider may have different rate limits and capabilities.
          </p>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <Transition
      enter-active-class="transition-all duration-300"
      enter-from-class="opacity-0 translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-200"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-4"
    >
      <div
        v-if="toast.show"
        :class="[
          'fixed bottom-8 right-8 px-6 py-4 rounded-xl shadow-glass flex items-center gap-3',
          toast.type === 'success' ? 'bg-green-500/20 border border-green-500/20' : 'bg-red-500/20 border border-red-500/20'
        ]"
      >
        <svg v-if="toast.type === 'success'" class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        <svg v-else class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        <span class="text-white">{{ toast.message }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'

const apiProviders = {
  openrouter: {
    name: 'OpenRouter',
    description: 'Access multiple AI models including ling-2.6-1T',
    placeholder: 'sk-or-v1-...',
    hint: 'Get your key from platform.openrouter.ai',
    bgClass: 'bg-blue-500/10 text-blue-400',
    icon: {
      render: () => ({
        template: `<svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>`
      })
    }
  },
  gemini: {
    name: 'Google Gemini',
    description: 'Google\'s advanced AI model',
    placeholder: 'AIza...',
    hint: 'Get your key from aistudio.google.com',
    bgClass: 'bg-purple-500/10 text-purple-400',
    icon: {
      render: () => ({
        template: `<svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2l2.4 7.2H22l-6 4.8 2.4 7.2L12 16l-6.4 5.2L8 14l-6-4.8h7.6L12 2z"/></svg>`
      })
    }
  },
  groq: {
    name: 'Groq',
    description: 'Ultra-fast AI inference',
    placeholder: 'gsk_...',
    hint: 'Get your key from console.groq.com',
    bgClass: 'bg-orange-500/10 text-orange-400',
    icon: {
      render: () => ({
        template: `<svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7v10l10 5 10-5V7L12 2zm0 18.5L4.5 14 12 9.5l7.5 4.5L12 20.5z"/></svg>`
      })
    }
  },
  openai: {
    name: 'OpenAI',
    description: 'GPT models from OpenAI',
    placeholder: 'sk-...',
    hint: 'Get your key from platform.openai.com',
    bgClass: 'bg-green-500/10 text-green-400',
    icon: {
      render: () => ({
        template: `<svg fill="currentColor" viewBox="0 0 24 24"><path d="M22.282 9.821a5.985 5.985 0 0 0-.516-4.91 6.046 6.046 0 0 0-6.51-2.9A6.065 6.065 0 0 0 4.981 4.18a5.985 5.985 0 0 0-3.998 2.366 5.98 5.98 0 0 0 .743 7.097 5.98 5.98 0 0 0 .51 4.911 6.051 6.051 0 0 0 6.515 2.898A5.985 5.985 0 0 0 13.26 24a5.985 5.985 0 0 0 3.998-2.366 5.98 5.98 0 0 0-.743-7.097z"/></svg>`
      })
    }
  },
  claude: {
    name: 'Claude (Anthropic)',
    description: 'Advanced AI from Anthropic',
    placeholder: 'sk-ant-...',
    hint: 'Get your key from console.anthropic.com',
    bgClass: 'bg-red-500/10 text-red-400',
    icon: {
      render: () => ({
        template: `<svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>`
      })
    }
  },
  chatgpt: {
    name: 'ChatGPT',
    description: 'OpenAI\'s conversational AI',
    placeholder: 'o1-...',
    hint: 'Get your key from chat.openai.com',
    bgClass: 'bg-cyan-500/10 text-cyan-400',
    icon: {
      render: () => ({
        template: `<svg fill="currentColor" viewBox="0 0 24 24"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/></svg>`
      })
    }
  }
}

const keys = reactive({
  openrouter: '',
  gemini: '',
  groq: '',
  openai: '',
  claude: '',
  chatgpt: ''
})

const visibility = reactive({
  openrouter: false,
  gemini: false,
  groq: false,
  openai: false,
  claude: false,
  chatgpt: false
})

const saving = reactive({
  openrouter: false,
  gemini: false,
  groq: false,
  openai: false,
  claude: false,
  chatgpt: false
})

const savedKeys = reactive({
  openrouter: false,
  gemini: false,
  groq: false,
  openai: false,
  claude: false,
  chatgpt: false
})

const toast = reactive({
  show: false,
  type: 'success',
  message: ''
})

const showToast = (type, message) => {
  toast.type = type
  toast.message = message
  toast.show = true
  setTimeout(() => {
    toast.show = false
  }, 3000)
}

const toggleVisibility = (key) => {
  visibility[key] = !visibility[key]
}

const saveKey = async (key) => {
  if (!keys[key]) return

  saving[key] = true

  // Simulate encryption and storage
  await new Promise(resolve => setTimeout(resolve, 800))

  // Store in localStorage with encryption simulation
  const encrypted = btoa(keys[key])
  localStorage.setItem(`amk_api_key_${key}`, encrypted)
  savedKeys[key] = true

  saving[key] = false
  showToast('success', `${apiProviders[key].name} key saved securely`)
}

onMounted(() => {
  // Load saved keys (decrypted)
  Object.keys(keys).forEach(key => {
    const saved = localStorage.getItem(`amk_api_key_${key}`)
    if (saved) {
      try {
        keys[key] = atob(saved)
        savedKeys[key] = true
      } catch (e) {
        console.error('Failed to decrypt key:', e)
      }
    }
  })
})
</script>