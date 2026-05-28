<template>
  <div class="max-w-4xl mx-auto">
    <!-- Hero Section -->
    <section class="text-center mb-16">
      <div class="w-24 h-24 rounded-3xl bg-gradient-to-br from-cyber-accent to-cyber-accent-light flex items-center justify-center mx-auto mb-8 shadow-glow">
        <span class="text-4xl font-bold text-white font-mono">⟨⟩</span>
      </div>
      <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">
        AMK AI Coder Platform
      </h1>
      <p class="text-xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
        Next-generation AI coding assistant with advanced deep thinking capabilities.
        Built for developers who demand excellence.
      </p>
    </section>

    <!-- Features Grid -->
    <section class="mb-16">
      <h2 class="text-2xl font-bold text-white text-center mb-8">Why Choose AMK AI?</h2>
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div v-for="feature in features" :key="feature.title" class="glass rounded-2xl p-6 hover:border-cyber-accent/30 transition-all">
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-cyber-accent/20 to-cyber-accent/5 flex items-center justify-center mb-4">
            <span v-html="feature.icon" class="w-6 h-6 text-cyber-accent" />
          </div>
          <h3 class="text-lg font-semibold text-white mb-2">{{ feature.title }}</h3>
          <p class="text-sm text-gray-400 leading-relaxed">{{ feature.description }}</p>
        </div>
      </div>
    </section>

    <!-- Tech Stack -->
    <section class="mb-16">
      <h2 class="text-2xl font-bold text-white text-center mb-8">Built With</h2>
      <div class="glass rounded-2xl p-8">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div v-for="tech in techStack" :key="tech.name" class="text-center">
            <div class="text-3xl mb-2">{{ tech.icon }}</div>
            <h4 class="font-medium text-white mb-1">{{ tech.name }}</h4>
            <p class="text-xs text-gray-500">{{ tech.category }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="text-center">
      <div class="glass rounded-3xl p-12 bg-gradient-to-r from-cyber-accent/10 to-transparent">
        <h2 class="text-3xl font-bold text-white mb-4">Ready to Start?</h2>
        <p class="text-gray-400 mb-8 max-w-lg mx-auto">
          Join thousands of developers using AMK AI to build better software faster.
        </p>
        <div class="flex flex-col sm:flex-row items-center justify-center gap-4">
          <RouterLink to="/auth" class="btn-primary px-8 py-4 text-lg">
            Get Started Free
          </RouterLink>
          <RouterLink to="/docs" class="btn-secondary px-8 py-4 text-lg">
            Read Documentation
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Version Info -->
    <div class="mt-16 text-center text-sm text-gray-500">
      <p>Version 1.0.0 • Built with Vue 3, FastAPI, and OpenRouter</p>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const features = [
  {
    title: 'Deep Thinking Mode',
    description: 'Advanced reasoning for complex architectural decisions and multi-step problem solving.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>`
  },
  {
    title: 'Multi-Provider Support',
    description: 'Seamlessly switch between OpenRouter, Gemini, Groq, Claude, and more.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>`
  },
  {
    title: 'File Intelligence',
    description: 'Upload documents, images, and code files for context-aware assistance.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>`
  },
  {
    title: 'Real-time Streaming',
    description: 'Experience instant responses with streaming text generation.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>`
  },
  {
    title: 'PWA Ready',
    description: 'Install as an app on any device with offline capabilities.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>`
  },
  {
    title: 'Secure & Private',
    description: 'Your API keys are encrypted locally. Firebase authentication keeps you safe.',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>`
  }
]

const techStack = [
  { name: 'Vue 3', icon: '🖖', category: 'Frontend' },
  { name: 'Vite', icon: '⚡', category: 'Build Tool' },
  { name: 'Tailwind', icon: '🎨', category: 'Styling' },
  { name: 'Three.js', icon: '🌐', category: '3D Graphics' },
  { name: 'Firebase', icon: '🔥', category: 'Auth' },
  { name: 'FastAPI', icon: '🐍', category: 'Backend' },
  { name: 'Supabase', icon: '💾', category: 'Storage' },
  { name: 'OpenRouter', icon: '🤖', category: 'AI' }
]
</script>