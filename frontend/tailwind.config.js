/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'cyber-dark': '#0a0a0f',
        'cyber-surface': '#12121a',
        'cyber-border': '#1e1e2e',
        'cyber-accent': '#6366f1',
        'cyber-accent-light': '#818cf8',
        'cyber-glow': 'rgba(99, 102, 241, 0.15)',
        'glass-bg': 'rgba(18, 18, 26, 0.7)',
        'glass-border': 'rgba(255, 255, 255, 0.08)',
      },
      backdropBlur: {
        'xs': '2px',
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'mono': ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'gradient-shift': 'gradient-shift 8s ease infinite',
        'thinking-orb': 'thinking-orb 4s ease-in-out infinite',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { opacity: '0.5', transform: 'scale(1)' },
          '50%': { opacity: '1', transform: 'scale(1.05)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'gradient-shift': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
        'thinking-orb': {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)', opacity: '0.8' },
          '25%': { transform: 'translate(10px, -10px) scale(1.1)', opacity: '1' },
          '50%': { transform: 'translate(-5px, 5px) scale(0.95)', opacity: '0.6' },
          '75%': { transform: 'translate(-10px, -5px) scale(1.05)', opacity: '0.9' },
        },
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
        'glass-hover': '0 8px 40px 0 rgba(99, 102, 241, 0.15)',
        'glow': '0 0 20px rgba(99, 102, 241, 0.4)',
        'glow-lg': '0 0 40px rgba(99, 102, 241, 0.6)',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}