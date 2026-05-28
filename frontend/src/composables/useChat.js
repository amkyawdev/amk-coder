import { ref, computed } from 'vue'

// Use HuggingFace Space FastAPI backend
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://amkyawdev-amk-coder-backend.hf.space'

export function useChat() {
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const thinkingMode = ref(false)
  const sessionId = ref('default-' + Date.now())

  const hasMessages = computed(() => messages.value.length > 0)

  const addMessage = (role, content) => {
    messages.value.push({
      id: Date.now().toString(),
      role,
      content,
      timestamp: new Date().toISOString()
    })
  }

  const updateLastMessage = (content) => {
    if (messages.value.length > 0) {
      const lastMessage = messages.value[messages.value.length - 1]
      if (lastMessage.role === 'assistant') {
        lastMessage.content = content
      }
    }
  }

  const sendMessage = async (content, options = {}) => {
    if (!content.trim() || isLoading.value) return

    isLoading.value = true
    error.value = null

    // Add user message
    addMessage('user', content)
    // Create assistant placeholder
    addMessage('assistant', '')

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          thinking_mode: thinkingMode.value,
          model: options.model || 'inclusionai/ling-2.6-1t:free',
          session_id: sessionId.value
        }),
      })

      if (!response.ok) {
        const data = await response.json().catch(() => ({}))
        throw new Error(data.detail || `HTTP ${response.status}: Request failed`)
      }

      const data = await response.json()
      // Replace placeholder with actual response
      messages.value[messages.value.length - 1].content = data.response

    } catch (err) {
      error.value = err.message || 'Failed to send message'
      // Remove empty message on error
      if (messages.value.length > 0 && !messages.value[messages.value.length - 1].content) {
        messages.value.pop()
      }
    } finally {
      isLoading.value = false
    }
  }

  const cancelRequest = () => {
    isLoading.value = false
  }

  const clearHistory = async () => {
    messages.value = []
    error.value = null
    sessionId.value = 'default-' + Date.now()
    
    // Call backend to clear session
    try {
      await fetch(`${API_BASE_URL}/api/clear?session_id=${sessionId.value}`, {
        method: 'POST'
      })
    } catch (e) {}
  }

  const toggleThinkingMode = () => {
    thinkingMode.value = !thinkingMode.value
  }

  return {
    messages,
    isLoading,
    error,
    thinkingMode,
    hasMessages,
    sendMessage,
    cancelRequest,
    clearHistory,
    toggleThinkingMode,
    addMessage
  }
}