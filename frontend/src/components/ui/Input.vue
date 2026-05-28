<template>
  <div class="relative">
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-300 mb-2">
      {{ label }}
    </label>
    <div class="relative">
      <input
        v-if="type !== 'textarea'"
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :autocomplete="autocomplete"
        :class="[
          'w-full px-4 py-3 rounded-xl bg-cyber-surface border border-cyber-border',
          'text-white placeholder-gray-500',
          'focus:outline-none focus:border-cyber-accent focus:ring-2 focus:ring-cyber-accent/20',
          'transition-all duration-200',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          iconLeft ? 'pl-11' : '',
          iconRight ? 'pr-11' : '',
          error ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20' : ''
        ]"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />
      <textarea
        v-else
        :id="id"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :rows="rows"
        :class="[
          'w-full px-4 py-3 rounded-xl bg-cyber-surface border border-cyber-border',
          'text-white placeholder-gray-500 resize-none',
          'focus:outline-none focus:border-cyber-accent focus:ring-2 focus:ring-cyber-accent/20',
          'transition-all duration-200',
          'disabled:opacity-50 disabled:cursor-not-allowed',
          error ? 'border-red-500/50 focus:border-red-500 focus:ring-red-500/20' : ''
        ]"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />

      <!-- Left Icon -->
      <div v-if="iconLeft" class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
        <slot name="icon-left" />
      </div>

      <!-- Right Icon -->
      <div v-if="iconRight" class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400">
        <slot name="icon-right" />
      </div>
    </div>

    <!-- Error Message -->
    <p v-if="error" class="mt-2 text-sm text-red-400">
      {{ error }}
    </p>

    <!-- Hint -->
    <p v-else-if="hint" class="mt-2 text-sm text-gray-500">
      {{ hint }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  label: String,
  placeholder: String,
  disabled: Boolean,
  error: String,
  hint: String,
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`
  },
  autocomplete: String,
  iconLeft: Boolean,
  iconRight: Boolean,
  rows: {
    type: Number,
    default: 4
  }
})

defineEmits(['update:modelValue', 'blur', 'focus'])
</script>