<template>
  <div class="h-[calc(100vh-8rem)] flex flex-col">
    <!-- Thinking Animation Overlay -->
    <Transition
      enter-active-class="transition-opacity duration-500"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition-opacity duration-300"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="isLoading && thinkingMode"
        class="absolute inset-0 z-10 pointer-events-none"
      >
        <ThinkingCanvas :active="isLoading && thinkingMode" />
        <div class="absolute bottom-32 left-1/2 -translate-x-1/2 flex items-center gap-3 px-6 py-3 rounded-full glass">
          <div class="w-3 h-3 rounded-full bg-cyber-accent animate-pulse" />
          <span class="text-sm text-gray-300">Deep thinking in progress...</span>
        </div>
      </div>
    </Transition>

    <!-- Chat Header -->
    <div class="flex items-center justify-between mb-4">
      <div>
        <h1 class="text-2xl font-bold text-white">Chat</h1>
        <p class="text-sm text-gray-400">Powered by advanced AI reasoning</p>
      </div>
      <div class="flex items-center gap-3">
        <!-- Thinking Mode Indicator -->
        <div
          v-if="thinkingMode"
          class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyber-accent/10 border border-cyber-accent/20"
        >
          <svg class="w-4 h-4 text-cyber-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          <span class="text-sm text-cyber-accent">Deep Thinking</span>
        </div>

        <!-- Clear Chat -->
        <button
          v-if="hasMessages"
          @click="clearHistory"
          class="p-2.5 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
          title="Clear chat"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Messages Container -->
    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto space-y-8 pb-4 pr-2"
    >
      <!-- Welcome Message -->
      <div
        v-if="!hasMessages && !isLoading"
        class="flex flex-col items-center justify-center h-full text-center"
      >
        <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-cyber-accent to-cyber-accent-light flex items-center justify-center mb-6">
          <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-white mb-3">Start a Conversation</h2>
        <p class="text-gray-400 max-w-md mb-8">
          Ask me anything about coding, architecture, debugging, or complex problem-solving.
          Toggle deep thinking for advanced reasoning.
        </p>

        <!-- Suggested Prompts -->
        <div class="flex flex-wrap justify-center gap-3">
          <button
            v-for="(prompt, index) in suggestedPrompts"
            :key="index"
            @click="usePrompt(prompt)"
            class="px-4 py-2 rounded-xl bg-cyber-surface border border-cyber-border text-sm text-gray-300 hover:text-white hover:border-cyber-accent/30 transition-all"
          >
            {{ prompt }}
          </button>
        </div>
      </div>

      <!-- Chat Messages -->
      <ChatBubble
        v-for="message in messages"
        :key="message.id"
        :content="message.content"
        :is-user="message.role === 'user'"
        :timestamp="message.timestamp"
      />
    </div>

    <!-- Input Area -->
    <div class="mt-4">
      <ChatInput
        ref="chatInput"
        :loading="isLoading"
        :thinking-mode="thinkingMode"
        :files="uploadedFiles"
        :uploading="uploading"
        :upload-progress="uploadProgress"
        @send="handleSend"
        @toggle-thinking="toggleThinkingMode"
        @upload="handleUpload"
        @remove-file="removeFile"
      />

      <!-- Error Display -->
      <div
        v-if="error"
        class="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-400 text-sm flex items-center gap-3"
      >
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ error }}
        <button
          v-if="isLoading"
          @click="cancelRequest"
          class="ml-auto px-3 py-1 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 text-xs"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { useChat } from '@/composables/useChat'
import { useStorage } from '@/composables/useStorage'
import ChatBubble from '@/components/chat/ChatBubble.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
import ThinkingCanvas from '@/components/three/ThinkingCanvas.vue'

const {
  messages,
  isLoading,
  error,
  thinkingMode,
  hasMessages,
  sendMessage,
  cancelRequest,
  clearHistory,
  toggleThinkingMode
} = useChat()

const {
  uploading,
  uploadProgress,
  uploadedFiles,
  uploadFile,
  clearFiles
} = useStorage()

const messagesContainer = ref(null)
const chatInput = ref(null)

const suggestedPrompts = [
  'Help me design a REST API',
  'Explain async/await patterns',
  'Debug my JavaScript code',
  'Review my Python architecture'
]

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

watch(messages, () => {
  scrollToBottom()
}, { deep: true })

watch(isLoading, (loading) => {
  if (loading) {
    scrollToBottom()
  }
})

const handleSend = async ({ text, files }) => {
  if (!text.trim()) return

  console.log('handleSend called with:', text)  // Debug log

  // Include file URLs in message if any
  let fullText = text
  if (files && files.length > 0) {
    const fileUrls = files.map(f => `File: ${f.name}\nURL: ${f.url}`).join('\n\n')
    fullText = `${text}\n\n[Attached Files]\n${fileUrls}`
  }

  await sendMessage(fullText)
  clearFiles()
}

const usePrompt = async (prompt) => {
  await sendMessage(prompt)
}

const handleUpload = async (files) => {
  for (const file of files) {
    await uploadFile(file)
  }
}

const removeFile = (index) => {
  uploadedFiles.value.splice(index, 1)
}

onMounted(() => {
  chatInput.value?.focus()
})
</script>