import { ref, computed } from 'vue'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

export function useChat() {
  const messages = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const thinkingMode = ref(false)
  const abortController = ref(null)

  const hasMessages = computed(() => messages.value.length > 0)

  const addMessage = (role, content, metadata = {}) => {
    messages.value.push({
      id: Date.now().toString(),
      role,
      content,
      metadata,
      timestamp: new Date().toISOString()
    })
  }

  const updateLastMessage = (content, metadata = {}) => {
    if (messages.value.length > 0) {
      const lastMessage = messages.value[messages.value.length - 1]
      if (lastMessage.role === 'assistant') {
        lastMessage.content += content
        lastMessage.metadata = { ...lastMessage.metadata, ...metadata }
      }
    }
  }

  const sendMessage = async (content, customApiKeys = null) => {
    if (!content.trim() || isLoading.value) return

    isLoading.value = true
    error.value = null

    // Add user message
    addMessage('user', content)

    // Create assistant message placeholder
    addMessage('assistant', '')

    // Setup abort controller for cancellation
    abortController.value = new AbortController()

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add Firebase ID token if available
          ...(customApiKeys?.idToken && { 'Authorization': `Bearer ${customApiKeys.idToken}` })
        },
        body: JSON.stringify({
          messages: messages.value.slice(0, -1).map(m => ({
            role: m.role,
            content: m.content
          })),
          message: content,
          thinking_mode: thinkingMode.value,
          custom_api_keys: customApiKeys ? {
            openrouter: customApiKeys.openrouter,
            gemini: customApiKeys.gemini,
            groq: customApiKeys.groq,
            openai: customApiKeys.openai,
            claude: customApiKeys.claude
          } : null
        }),
        signal: abortController.value.signal
      })

      if (!response.ok) {
        const data = await response.json().catch(() => ({}))
        throw new Error(data.error || `HTTP ${response.status}: Request failed`)
      }

      // Handle streaming response
      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') {
              break
            }
            try {
              const parsed = JSON.parse(data)
              if (parsed.content) {
                updateLastMessage(parsed.content)
              }
              if (parsed.thinking) {
                // Handle thinking content separately if needed
              }
            } catch (e) {
              // Ignore parse errors for incomplete chunks
            }
          }
        }
      }

    } catch (err) {
      if (err.name === 'AbortError') {
        error.value = 'Request cancelled'
      } else {
        error.value = err.message || 'Failed to send message'
        // Remove the empty assistant message on error
        if (messages.value.length > 0 && !messages.value[messages.value.length - 1].content) {
          messages.value.pop()
        }
      }
    } finally {
      isLoading.value = false
      abortController.value = null
    }
  }

  const cancelRequest = () => {
    if (abortController.value) {
      abortController.value.abort()
    }
  }

  const clearHistory = () => {
    messages.value = []
    error.value = null
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