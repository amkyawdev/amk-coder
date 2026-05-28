<template>
  <div
    :class="[
      'chat-bubble relative group',
      isUser ? 'chat-bubble-user' : 'chat-bubble-assistant'
    ]"
  >
    <!-- Content -->
    <div class="prose prose-invert prose-sm max-w-none">
      <div v-html="formattedContent" />
    </div>

    <!-- Timestamp -->
    <div
      v-if="timestamp"
      :class="[
        'absolute -bottom-5 text-xs opacity-0 group-hover:opacity-60 transition-opacity',
        isUser ? 'right-2' : 'left-2'
      ]"
    >
      {{ formatTime(timestamp) }}
    </div>

    <!-- Copy Button -->
    <button
      v-if="!isUser"
      @click="copyContent"
      :class="[
        'absolute top-2 right-2 p-1.5 rounded-lg opacity-0 group-hover:opacity-60 transition-all',
        'hover:bg-white/10 hover:opacity-100'
      ]"
      title="Copy to clipboard"
    >
      <svg v-if="!copied" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
      </svg>
      <svg v-else class="w-4 h-4 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  content: {
    type: String,
    default: ''
  },
  isUser: {
    type: Boolean,
    default: false
  },
  timestamp: String
})

const copied = ref(false)

const formattedContent = computed(() => {
  if (!props.content) return ''
  
  // Simple markdown-like formatting
  let text = props.content
  
  // Code blocks
  text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre class="bg-cyber-dark rounded-lg p-3 my-2 overflow-x-auto"><code>$2</code></pre>')
  
  // Inline code
  text = text.replace(/`([^`]+)`/g, '<code class="bg-cyber-dark/50 px-1.5 py-0.5 rounded text-cyber-accent-light">$1</code>')
  
  // Bold
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-semibold">$1</strong>')
  
  // Italic
  text = text.replace(/\*([^*]+)\*/g, '<em class="italic">$1</em>')
  
  // Links
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-cyber-accent hover:underline" target="_blank" rel="noopener">$1</a>')
  
  // Line breaks (preserve paragraphs)
  text = text.replace(/\n\n/g, '</p><p class="my-2">')
  text = text.replace(/\n/g, '<br>')
  text = `<p>${text}</p>`
  
  return text
})

const formatTime = (isoString) => {
  const date = new Date(isoString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

const copyContent = async () => {
  try {
    await navigator.clipboard.writeText(props.content)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>