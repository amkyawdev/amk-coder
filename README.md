# AMK AI Coder Platform

Next-generation AI coding assistant with advanced deep thinking capabilities, built with Vue 3, FastAPI, and OpenRouter.

## Features

- 🤖 **AI Chat** - Standard and Deep Thinking modes for complex problem-solving
- 🔐 **Firebase Authentication** - Secure email/password and Google OAuth
- 📁 **File Uploads** - Supabase storage for documents, images, and code files
- 🔑 **Multi-Provider Support** - OpenRouter, Gemini, Groq, Claude integration
- 🎨 **Modern UI** - Cyber-minimalism design with glassmorphism effects
- 📱 **PWA Ready** - Install as app with offline capabilities
- 🌐 **Three.js Animations** - Immersive visual experience

## Tech Stack

### Frontend (Vercel)
- Vue 3 (Composition API, `<script setup>`)
- Vite
- Tailwind CSS
- Three.js
- Firebase Auth
- Supabase Storage
- vite-plugin-pwa

### Backend (Railway)
- Python FastAPI
- Firebase Admin SDK
- OpenRouter API
- httpx for async HTTP

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Firebase Project
- Supabase Project (optional)
- OpenRouter API Key

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm run dev
```

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Run development server
uvicorn app.main:app --reload --port 8000
```

## Environment Variables

### Frontend (.env)
```env
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_key
VITE_API_URL=http://localhost:8000
```

### Backend (.env)
```env
# Firebase (for server-side token verification)
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\n..."
FIREBASE_CLIENT_EMAIL=firebase-adminsdk@your_project.iam.gserviceaccount.com

# AI Providers
OPENROUTER_API_KEY=sk-or-v1-...
GEMINI_API_KEY=AIza...
GROQ_API_KEY=gsk_...

# Optional
DEBUG=false
```

## Project Structure

```
amk-ai-coder-platform/
├── frontend/
│   ├── public/
│   │   ├── favicon.svg
│   │   ├── manifest.json
│   │   └── sw.js
│   ├── src/
│   │   ├── assets/main.css
│   │   ├── components/
│   │   │   ├── ui/          # Button, Input, Dialog
│   │   │   ├── chat/        # ChatBubble, ChatInput
│   │   │   └── three/        # ThinkingCanvas, CoderCanvas
│   │   ├── composables/      # useAuth, useStorage, useChat
│   │   ├── router/
│   │   └── views/           # GetStarted, Auth, Chat, etc.
│   ├── index.html
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   └── chat.py
│   │   └── utils/
│   │       └── prompts.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── README.md
└── LICENSE
```

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy with automatic CI/CD

```bash
# Vercel CLI
npm i -g vercel
vercel
```

### Backend (Railway)

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Railway auto-detects Dockerfile

```bash
# Railway CLI
npm i -g @railway/cli
railway login
railway init
railway up
```

## API Endpoints

### Authentication
- `POST /api/auth/verify` - Verify Firebase token
- `GET /api/auth/status` - Get auth status
- `GET /api/auth/me` - Get user info

### Chat
- `POST /api/chat` - Send message (streaming)
- `POST /api/chat/non-stream` - Send message (non-streaming)
- `GET /api/chat/models` - List available models

## License

MIT License - see LICENSE file for details.

---

Built with ❤️ by AMK AI Team