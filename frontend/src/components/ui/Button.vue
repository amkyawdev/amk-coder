<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="[
      'relative inline-flex items-center justify-center gap-2 font-medium transition-all duration-300',
      sizeClasses,
      variantClasses,
      { 'cursor-not-allowed opacity-50': disabled || loading }
    ]"
  >
    <span v-if="loading" :class="spinnerClasses" />
    <slot v-else />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'ghost', 'danger'].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  },
  type: {
    type: String,
    default: 'button'
  },
  disabled: Boolean,
  loading: Boolean
})

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'px-3 py-1.5 text-sm rounded-lg',
    md: 'px-5 py-2.5 text-base rounded-xl',
    lg: 'px-7 py-3.5 text-lg rounded-xl'
  }
  return sizes[props.size]
})

const variantClasses = computed(() => {
  const variants = {
    primary: 'bg-gradient-to-r from-cyber-accent to-cyber-accent-light text-white shadow-glow hover:shadow-glow-lg active:scale-95',
    secondary: 'border border-glass-border bg-glass-bg backdrop-blur-md text-white hover:border-cyber-accent/50 hover:bg-cyber-surface active:scale-95',
    ghost: 'text-gray-400 hover:text-white hover:bg-white/5',
    danger: 'bg-red-500/20 text-red-400 border border-red-500/30 hover:bg-red-500/30 active:scale-95'
  }
  return variants[props.variant]
})

const spinnerClasses = computed(() => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  }
  return `w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin`
})
</script>