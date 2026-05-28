<template>
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-white mb-2">Documentation</h1>
      <p class="text-gray-400">Everything you need to know about AMK AI Coder Platform</p>
    </div>

    <!-- Table of Contents -->
    <nav class="glass rounded-2xl p-6 mb-8">
      <h2 class="text-lg font-semibold text-white mb-4">Quick Navigation</h2>
      <div class="grid md:grid-cols-2 gap-3">
        <a
          v-for="(section, index) in sections"
          :key="index"
          :href="`#${section.id}`"
          class="flex items-center gap-3 px-4 py-3 rounded-xl text-gray-400 hover:text-white hover:bg-white/5 transition-all"
        >
          <span class="w-8 h-8 rounded-lg bg-cyber-accent/10 flex items-center justify-center text-cyber-accent text-sm font-bold">
            {{ index + 1 }}
          </span>
          {{ section.title }}
        </a>
      </div>
    </nav>

    <!-- Sections -->
    <div class="space-y-8">
      <!-- Getting Started -->
      <section id="getting-started" class="glass rounded-2xl p-6">
        <h2 class="text-2xl font-bold text-white mb-4 flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-cyber-accent/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-cyber-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </span>
          Getting Started
        </h2>
        
        <div class="prose prose-invert max-w-none space-y-4">
          <h3 class="text-lg font-semibold text-white">Authentication</h3>
          <p class="text-gray-400 leading-relaxed">
            To access the AMK AI Coder Platform, you need to create an account or sign in with your existing credentials.
            We support Email/Password authentication and Google OAuth for your convenience.
          </p>

          <h3 class="text-lg font-semibold text-white">First Steps</h3>
          <ol class="list-decimal list-inside space-y-2 text-gray-400">
            <li>Navigate to the Auth page using the sidebar or by clicking "Sign In"</li>
            <li>Create a new account or sign in with Google</li>
            <li>Configure your API keys in the API Keys section</li>
            <li>Start chatting with the AI assistant</li>
          </ol>

          <div class="p-4 rounded-xl bg-cyber-surface/50 border border-glass-border">
            <p class="text-sm text-gray-400">
              <strong class="text-white">Pro Tip:</strong> You can use the platform without configuring additional API keys.
              By default, the OpenRouter integration provides access to multiple AI models.
            </p>
          </div>
        </div>
      </section>

      <!-- Chat Features -->
      <section id="chat-features" class="glass rounded-2xl p-6">
        <h2 class="text-2xl font-bold text-white mb-4 flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </span>
          Chat Features
        </h2>

        <div class="space-y-6">
          <div>
            <h3 class="text-lg font-semibold text-white mb-2">Standard Mode</h3>
            <p class="text-gray-400 leading-relaxed">
              The default chat mode provides quick, responsive AI assistance for general questions,
              code generation, and problem-solving. Perfect for rapid iterations and straightforward queries.
            </p>
          </div>

          <div>
            <h3 class="text-lg font-semibold text-white mb-2">Deep Thinking Mode</h3>
            <p class="text-gray-400 leading-relaxed">
              Toggle this mode for complex reasoning tasks. When enabled, the AI engages in extended
              chain-of-thought reasoning, making it ideal for:
            </p>
            <ul class="list-disc list-inside mt-3 space-y-2 text-gray-400">
              <li>System architecture design</li>
              <li>Algorithm optimization</li>
              <li>Debugging complex issues</li>
              <li>Code review and refactoring</li>
              <li>Multi-step problem solving</li>
            </ul>
          </div>

          <div class="p-4 rounded-xl bg-gradient-to-r from-cyber-accent/10 to-transparent border border-cyber-accent/20">
            <p class="text-sm text-gray-300">
              <strong class="text-cyber-accent">Note:</strong> Deep Thinking mode may take longer to respond
              as it involves more extensive processing and reasoning steps.
            </p>
          </div>
        </div>
      </section>

      <!-- File Uploads -->
      <section id="file-uploads" class="glass rounded-2xl p-6">
        <h2 class="text-2xl font-bold text-white mb-4 flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-green-500/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </span>
          File Uploads
        </h2>

        <p class="text-gray-400 mb-4">
          AMK AI supports file uploads for context-aware assistance. You can attach:
        </p>
        <ul class="list-disc list-inside space-y-2 text-gray-400 mb-4">
          <li><strong class="text-white">Images:</strong> PNG, JPG, GIF, SVG</li>
          <li><strong class="text-white">Documents:</strong> PDF, TXT, MD, JSON</li>
          <li><strong class="text-white">Code Files:</strong> PY, JS, TS, VUE, and more</li>
        </ul>
        <p class="text-gray-400">
          Files are uploaded to Supabase Storage and the URLs are sent with your message
          for context-aware AI processing. Each file shows an upload progress indicator.
        </p>
      </section>

      <!-- API Configuration -->
      <section id="api-config" class="glass rounded-2xl p-6">
        <h2 class="text-2xl font-bold text-white mb-4 flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-orange-500/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
            </svg>
          </span>
          API Configuration
        </h2>

        <div class="space-y-4">
          <p class="text-gray-400">
            Configure your own API keys for enhanced capabilities. Keys are encrypted and stored locally.
          </p>

          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="border-b border-cyber-border">
                  <th class="py-3 px-4 text-sm font-semibold text-white">Provider</th>
                  <th class="py-3 px-4 text-sm font-semibold text-white">Models</th>
                  <th class="py-3 px-4 text-sm font-semibold text-white">Best For</th>
                </tr>
              </thead>
              <tbody class="text-gray-400 text-sm">
                <tr class="border-b border-cyber-border/50">
                  <td class="py-3 px-4">OpenRouter</td>
                  <td class="py-3 px-4">Multiple including ling-2.6-1T</td>
                  <td class="py-3 px-4">Versatile, multi-model access</td>
                </tr>
                <tr class="border-b border-cyber-border/50">
                  <td class="py-3 px-4">Gemini</td>
                  <td class="py-3 px-4">Gemini Pro, Ultra</td>
                  <td class="py-3 px-4">Long context, multimodal</td>
                </tr>
                <tr class="border-b border-cyber-border/50">
                  <td class="py-3 px-4">Groq</td>
                  <td class="py-3 px-4">Llama, Mixtral</td>
                  <td class="py-3 px-4">Fast inference</td>
                </tr>
                <tr>
                  <td class="py-3 px-4">Claude</td>
                  <td class="py-3 px-4">Claude 3.5, Opus</td>
                  <td class="py-3 px-4">Long-form reasoning</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- Troubleshooting -->
      <section id="troubleshooting" class="glass rounded-2xl p-6">
        <h2 class="text-2xl font-bold text-white mb-4 flex items-center gap-3">
          <span class="w-10 h-10 rounded-xl bg-red-500/10 flex items-center justify-center">
            <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </span>
          Troubleshooting
        </h2>

        <div class="space-y-4">
          <div class="p-4 rounded-xl bg-cyber-surface/50">
            <h4 class="font-semibold text-white mb-2">Response too slow</h4>
            <p class="text-sm text-gray-400">
              Try using Groq for faster inference, or switch to Standard mode if Deep Thinking
              isn't necessary for your query.
            </p>
          </div>

          <div class="p-4 rounded-xl bg-cyber-surface/50">
            <h4 class="font-semibold text-white mb-2">File upload fails</h4>
            <p class="text-sm text-gray-400">
              Ensure your Supabase bucket is properly configured and your internet connection is stable.
              Check file size limits (max 10MB).
            </p>
          </div>

          <div class="p-4 rounded-xl bg-cyber-surface/50">
            <h4 class="font-semibold text-white mb-2">Authentication issues</h4>
            <p class="text-sm text-gray-400">
              Clear your browser cache and cookies, then try signing in again.
              Ensure your Firebase configuration is correct.
            </p>
          </div>
        </div>
      </section>
    </div>

    <!-- Footer -->
    <div class="mt-12 text-center">
      <p class="text-gray-500 text-sm">
        Need more help? Check the
        <a href="https://github.com" target="_blank" rel="noopener" class="text-cyber-accent hover:underline">GitHub repository</a>
        or submit an issue.
      </p>
    </div>
  </div>
</template>

<script setup>
const sections = [
  { id: 'getting-started', title: 'Getting Started' },
  { id: 'chat-features', title: 'Chat Features' },
  { id: 'file-uploads', title: 'File Uploads' },
  { id: 'api-config', title: 'API Configuration' },
  { id: 'troubleshooting', title: 'Troubleshooting' }
]
</script>