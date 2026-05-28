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
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="glass rounded-2xl p-6 hover:border-cyber-accent/30 transition-all"
        >
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-cyber-accent/20 to-cyber-accent/5 flex items-center justify-center mb-4">
            <component :is="feature.icon" class="w-6 h-6 text-cyber-accent" />
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
          <div
            v-for="(tech, index) in techStack"
            :key="index"
            class="text-center"
          >
            <div class="w-16 h-16 rounded-2xl bg-cyber-surface mx-auto mb-3 flex items-center justify-center">
              <span class="text-2xl">{{ tech.icon }}</span>
            </div>
            <h4 class="font-medium text-white mb-1">{{ tech.name }}</h4>
            <p class="text-xs text-gray-500">{{ tech.category }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Architecture Overview -->
    <section class="mb-16">
      <h2 class="text-2xl font-bold text-white text-center mb-8">Architecture</h2>
      <div class="glass rounded-2xl p-6">
        <div class="relative">
          <!-- Architecture Diagram -->
          <div class="flex flex-col md:flex-row items-center justify-center gap-4">
            <div class="glass rounded-xl p-4 text-center w-40">
              <div class="text-3xl mb-2">🎨</div>
              <h4 class="font-semibold text-white text-sm">Frontend</h4>
              <p class="text-xs text-gray-400">Vue 3 + Vite</p>
            </div>

            <div class="hidden md:block">
              <svg class="w-8 h-8 text-cyber-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </div>

            <div class="md:hidden">
              <svg class="w-8 h-8 text-cyber-accent rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </div>

            <div class="glass rounded-xl p-4 text-center w-40 border-cyber-accent/30">
              <div class="text-3xl mb-2">⚡</div>
              <h4 class="font-semibold text-white text-sm">Backend</h4>
              <p class="text-xs text-gray-400">FastAPI + Railway</p>
            </div>

            <div class="hidden md:block">
              <svg class="w-8 h-8 text-cyber-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
            </div>

            <div class="md:hidden">
              <svg class="w-8 h-8 text-cyber-accent rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
              </svg>
            </div>

            <div class="glass rounded-xl p-4 text-center w-40">
              <div class="text-3xl mb-2">🤖</div>
              <h4 class="font-semibold text-white text-sm">AI Providers</h4>
              <p class="text-xs text-gray-400">OpenRouter + Others</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="mb-16">
      <h2 class="text-2xl font-bold text-white text-center mb-8">Development Team</h2>
      <div class="glass rounded-2xl p-8 text-center">
        <p class="text-gray-400 leading-relaxed mb-6">
          AMK AI Coder Platform is developed by a team of passionate engineers dedicated to
          building the next generation of AI-powered development tools.
        </p>
        <div class="flex items-center justify-center gap-4">
          <a
            href="#"
            class="w-12 h-12 rounded-xl bg-cyber-surface flex items-center justify-center text-gray-400 hover:text-white hover:bg-cyber-accent/20 transition-all"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
          </a>
          <a
            href="#"
            class="w-12 h-12 rounded-xl bg-cyber-surface flex items-center justify-center text-gray-400 hover:text-white hover:bg-cyber-accent/20 transition-all"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
          </a>
          <a
            href="#"
            class="w-12 h-12 rounded-xl bg-cyber-surface flex items-center justify-center text-gray-400 hover:text-white hover:bg-cyber-accent/20 transition-all"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
            </svg>
          </a>
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
          <RouterLink
            to="/auth"
            class="btn-primary px-8 py-4 text-lg"
          >
            Get Started Free
          </RouterLink>
          <RouterLink
            to="/docs"
            class="btn-secondary px-8 py-4 text-lg"
          >
            Read Documentation
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Version Info -->
    <div class="mt-16 text-center text-sm text-gray-500">
      <p>Version 1.0.0 • Built with ❤️ using Vue 3, FastAPI, and OpenRouter</p>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const features = [
  {
    title: 'Deep Thinking Mode',
    description: 'Advanced reasoning for complex architectural decisions and multi-step problem solving.',
    icon: {
      render: () => ({
        template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>`
      })
    }
  },
  {
    title: 'Multi-Provider Support',
    description: 'Seamlessly switch between OpenRouter, Gemini, Groq, Claude, and more.',
    icon: {
      render: () => ({
        template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>`
      })
    }
  },
  {
    title: 'File Intelligence',
    description: 'Upload documents, images, and code files for context-aware assistance.',
    icon: {
      render: () => ({
        template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>`
      })
    }
  },
  {
    title: 'Real-time Streaming',
    description: 'Experience instant responses with streaming text generation.',
    icon: {
      render: () => ({
        template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>`
      })
    }
  },
  {
    title: 'PWA Ready',
    description: 'Install as an app on any device with offline capabilities.',
    icon: {
      render: () => ({
        template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>`
      })
    }
  },
  {
    title: 'Secure & Private',
    description: 'Your API keys are encrypted locally. Firebase authentication keeps you safe.',
    icon: {
      render: () => ({
        template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>`
      })
    }
  }
]

const techStack = [
  { name: 'Vue 3', icon: '🖖', category: 'Frontend Framework' },
  { name: 'Vite', icon: '⚡', category: 'Build Tool' },
  { name: 'Tailwind CSS', icon: '🎨', category: 'Styling' },
  { name: 'Three.js', icon: '🌐', category: '3D Graphics' },
  { name: 'Firebase', icon: '🔥', category: 'Authentication' },
  { name: 'Supabase', icon: '💾', category: 'Storage' },
  { name: 'FastAPI', icon: '🐍', category: 'Backend' },
  { name: 'OpenRouter', icon: '🤖', category: 'AI Integration' }
]
</script>