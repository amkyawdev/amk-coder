<template>
  <div class="relative min-h-[calc(100vh-8rem)] flex items-center justify-center overflow-hidden">
    <!-- Three.js Background -->
    <div class="absolute inset-0 z-0">
      <CoderCanvas />
    </div>

    <!-- Gradient Overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-cyber-dark via-transparent to-transparent z-10" />

    <!-- Content -->
    <div class="relative z-20 text-center px-4 max-w-4xl mx-auto">
      <!-- Hero Badge -->
      <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8 animate-float">
        <span class="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
        <span class="text-sm text-gray-300">Powered by Advanced AI</span>
      </div>

      <!-- Main Title -->
      <h1 class="text-5xl md:text-7xl font-bold mb-6">
        <span class="text-gradient">Build Faster</span>
        <br />
        <span class="text-gradient-accent">Think Deeper</span>
      </h1>

      <!-- Description -->
      <p class="text-lg md:text-xl text-gray-400 mb-10 max-w-2xl mx-auto leading-relaxed">
        Your next-generation AI coding assistant with advanced deep thinking capabilities.
        Transform ideas into production-ready code with intelligent context awareness.
      </p>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
        <RouterLink
          to="/auth"
          class="btn-primary px-8 py-4 text-lg flex items-center gap-3 group"
        >
          <svg class="w-6 h-6 transition-transform group-hover:scale-110" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Start Building
        </RouterLink>
        <RouterLink
          to="/docs"
          class="btn-secondary px-8 py-4 text-lg flex items-center gap-3 group"
        >
          <svg class="w-5 h-5 transition-transform group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Read Docs
        </RouterLink>
      </div>

      <!-- Feature Cards -->
      <div class="mt-20 grid md:grid-cols-3 gap-6">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="glass rounded-2xl p-6 text-left hover:border-cyber-accent/30 transition-all duration-300 group"
        >
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-cyber-accent/20 to-cyber-accent/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
            <span v-html="feature.icon" class="w-6 h-6 text-cyber-accent" />
          </div>
          <h3 class="text-lg font-semibold text-white mb-2">{{ feature.title }}</h3>
          <p class="text-sm text-gray-400 leading-relaxed">{{ feature.description }}</p>
        </div>
      </div>

      <!-- Stats -->
      <div class="mt-16 glass rounded-2xl p-6 flex flex-wrap justify-center gap-8 md:gap-16">
        <div v-for="(stat, index) in stats" :key="index" class="text-center">
          <div class="text-3xl md:text-4xl font-bold text-gradient-accent mb-1">{{ stat.value }}</div>
          <div class="text-sm text-gray-400">{{ stat.label }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import CoderCanvas from '@/components/three/CoderCanvas.vue'

const features = [
  {
    title: 'Deep Thinking Mode',
    description: 'Engage advanced reasoning capabilities for complex problem-solving and architectural decisions.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>`
  },
  {
    title: 'Multi-Platform Keys',
    description: 'Seamlessly integrate with Gemini, Groq, OpenAI, Claude, and other AI providers.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>`
  },
  {
    title: 'File Intelligence',
    description: 'Upload documents, code files, and images for context-aware AI assistance.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>`
  }
]

const stats = [
  { value: '50+', label: 'Languages Supported' },
  { value: '2M+', label: 'Tokens Context' },
  { value: '99.9%', label: 'Uptime' }
]
</script>