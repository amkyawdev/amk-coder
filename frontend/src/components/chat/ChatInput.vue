<template>
  <div :class="['floating-input glass rounded-2xl p-4 transition-all duration-300', { 'active': isActive }]">
    <!-- Thinking Mode Toggle -->
    <div class="flex items-center justify-between mb-3 pb-3 border-b border-glass-border">
      <span class="text-sm text-gray-400">Deep Thinking</span>
      <button
        @click="$emit('toggle-thinking')"
        :class="['thinking-toggle', { active: thinkingMode }]"
        role="switch"
        :aria-checked="thinkingMode"
      >
        <span class="sr-only">Toggle thinking mode</span>
      </button>
    </div>

    <!-- File Upload Area -->
    <div
      v-if="files.length > 0 || uploading"
      class="mb-3 space-y-2"
    >
      <div
        v-for="(file, index) in files"
        :key="index"
        class="flex items-center gap-3 p-2 rounded-lg bg-cyber-surface/50"
      >
        <svg class="w-5 h-5 text-cyber-accent flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span class="flex-1 text-sm text-gray-300 truncate">{{ file.name }}</span>
        <button
          @click="removeFile(index)"
          class="p-1 rounded hover:bg-white/10 text-gray-400 hover:text-white"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Upload Progress -->
      <div v-if="uploading" class="space-y-1">
        <div class="flex items-center justify-between text-xs">
          <span class="text-gray-400">Uploading...</span>
          <span class="text-cyber-accent">{{ uploadProgress }}%</span>
        </div>
        <div class="progress-bar">
          <div class="progress-bar-fill" :style="{ width: `${uploadProgress}%` }" />
        </div>
      </div>
    </div>

    <!-- Input Container -->
    <div class="flex items-end gap-3">
      <!-- File Upload Button -->
      <button
        @click="triggerFileInput"
        class="p-2.5 rounded-xl bg-cyber-surface border border-cyber-border text-gray-400 hover:text-white hover:border-cyber-accent/50 transition-all"
        title="Attach files"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
        </svg>
      </button>

      <input
        ref="fileInput"
        type="file"
        multiple
        class="hidden"
        @change="handleFileSelect"
        accept="image/*,.pdf,.txt,.md,.json,.py,.js,.ts,.vue"
      />

      <!-- Text Input -->
      <div class="flex-1">
        <textarea
          ref="inputRef"
          v-model="inputText"
          @keydown.enter.exact.prevent="handleSend"
          @input="autoResize"
          placeholder="Ask anything..."
          rows="1"
          :disabled="loading"
          class="w-full px-4 py-3 bg-transparent border-none text-white placeholder-gray-500 resize-none focus:outline-none disabled:opacity-50"
          style="max-height: 200px; min-height: 24px;"
        />
      </div>

      <!-- Send Button -->
      <button
        @click="handleSend"
        :disabled="!canSend"
        :class="[
          'p-3 rounded-xl transition-all duration-300',
          canSend
            ? 'bg-gradient-to-r from-cyber-accent to-cyber-accent-light text-white shadow-glow hover:shadow-glow-lg active:scale-95'
            : 'bg-cyber-surface text-gray-500 cursor-not-allowed'
        ]"
      >
        <svg v-if="loading" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
        </svg>
      </button>
    </div>

    <!-- Hint -->
    <p class="mt-2 text-xs text-gray-500 text-center">
      Press Enter to send, Shift+Enter for new line
    </p>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'

const props = defineProps({
  loading: Boolean,
  thinkingMode: Boolean,
  files: {
    type: Array,
    default: () => []
  },
  uploading: Boolean,
  uploadProgress: Number
})

const emit = defineEmits(['send', 'toggle-thinking', 'upload'])

const inputText = ref('')
const inputRef = ref(null)
const fileInput = ref(null)
const isActive = ref(false)

const canSend = computed(() => {
  return (inputText.value.trim() || props.files.length > 0) && !props.loading
})

const handleSend = () => {
  if (!canSend.value) return

  emit('send', {
    text: inputText.value.trim(),
    files: props.files
  })

  inputText.value = ''
  nextTick(() => {
    if (inputRef.value) {
      inputRef.value.style.height = 'auto'
    }
  })
}

const autoResize = () => {
  if (inputRef.value) {
    inputRef.value.style.height = 'auto'
    inputRef.value.style.height = Math.min(inputRef.value.scrollHeight, 200) + 'px'
  }
}

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (e) => {
  const files = Array.from(e.target.files || [])
  if (files.length > 0) {
    emit('upload', files)
  }
  // Reset input
  e.target.value = ''
}

const removeFile = (index) => {
  emit('remove-file', index)
}

// Focus input on mount
defineExpose({
  focus: () => inputRef.value?.focus()
})
</script>