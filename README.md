# Aether UI

AI UX + Frontend Engineering Agent for generating production-grade websites and SaaS dashboards from natural language prompts.

## What is scaffolded

- `apps/web`: Next.js 15 App Router UI with Supabase Auth hooks, dashboard, chat workspace, live preview panel, Zustand state, Tailwind, and shadcn-style primitives.
- `backend`: FastAPI service with typed agent contracts, generation orchestration, Server-Sent Events streaming, and provider adapters for mock, OpenRouter, and Ollama.
- `supabase/migrations`: PostgreSQL schema with RLS, indexes, storage bucket setup, and pgvector memory tables.

## Local setup

1. Copy `.env.example` to `.env.local` in `apps/web` and `.env` in the repo root or backend runtime environment.
2. Fill in your Supabase project URL and keys.
3. Apply the SQL migration in `supabase/migrations/001_initial_schema.sql` to your Supabase project.
4. Install dependencies:

```bash
npm install
pip install -e ".[dev]"
```

5. Run the services:

```bash
npm run dev
npm run backend:dev
```

The MVP currently includes the structured shell and deterministic generation pipeline needed to connect live models and preview execution safely.