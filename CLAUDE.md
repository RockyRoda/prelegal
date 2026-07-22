# Prelegal Project
## Overview

This is a Saas product to allaow usaers to draft legal agreemants based on templates in the templates directory. The users can carry an AI chat in order to establish what document they want and how to fill in the fields. The available documents are covered in the catalog.json file in the project root,included here:
@catalog.json
V1 only supports the Mutual NDA document; see Implementation Status below for what has been built so far.
## Development Process

when instructed to build a feature:
1. Use your Atlassian tools to read the feature instructions from Jira
1. Develop the feature - do not skip and step from the feature-dev 7 step process
1. Thoroughly tes the feature with unit tests and integeration tests and fix any issues
1. Submit a PR using your github tools

## Ai Design

When writing code to make calls to LLMs, use your Crebas skill to use LiteLLM via OpoenRouter to the openai/gpt-oss-20b:free model with Cerebas as the inference provider. You should use structured Outputs so that you can interpret the results and populate fiedls in the legal document.

There is an OPENROUTER_API_KEY in the .env file in the project root.

## Technical Design

The entire project should be packaged into a Docker container.
The Backend should be in backend/ and be a uv project, using FastAPI.
The frontend should be in frontend/
The database should use SQLLite and be created from scratch each time the Docker container is brought up, allowing for a suers table with a sign up and a sign in.
Consider statically building the frontend and serving it via FastAPI, if that will work.
There should be scripts in scripts/ for:
```bash
# Mac
scripts/start-mac.sh    # Start
scripts/stop-mac.sh     # Stop

# linux
scripts/start-linux.sh
scripts/stop-linux.sh

# Windows
scripts/start-windows.ps1
scripts/stop-windows.ps1
```
Backend available at http://localhost:8000

## Color scheme

- Accent Yellow `#ecad0a` — accent lines, highlights
- Blue Primary `#209dd7` — links, key sections
- Purple Secondary `#753991` — submit buttons, important actions
- Dark Navy `#032147` — main headings
- Gray Text `#888888` — supporting text, labels

## Implementation Status (as of 2026-07-21)

**Backend** (`backend/`, FastAPI + uv, Python >=3.12):
- SQLite database wiped and recreated on every app startup (`app/db.py`), single `users` table.
- `/api/auth/signup` and `/api/auth/signin` (`app/auth.py`) — fake/passwordless login, matched by email only.
- `/api/nda/chat` (`app/nda_chat.py` + `app/llm.py`) — stateless NDA chat endpoint. Each call sends the full message history and current NDA field values to `openai/gpt-oss-20b:free` via LiteLLM/OpenRouter/Cerebras (per the Cerebras skill) and returns the assistant's reply plus the complete updated field set.
  - **Known limitation**: this free model does not reliably honor structured-output constraints. The endpoint retries up to 3 times on malformed JSON or provider errors before returning a `502`; even so, only roughly 1 in 5 real requests succeed on the first attempt in testing. Revisit the model/schema if this proves too unreliable in practice.
  - `litellm` is pinned to `1.70.0` (not the latest) because newer releases bundle a Rust extension (`litellm-rust`) that failed to build on this machine (no MSVC/Rust toolchain installed). Re-evaluate the pin if that toolchain becomes available.
- `/api/health` endpoint. CORS open to `http://localhost:3000`.
- Tests in `backend/tests/test_auth.py` and `backend/tests/test_nda_chat.py`, run with pytest.

**Frontend** (`frontend/`, Next.js 16 + React 19 + Tailwind 4):
- `LoginScreen.tsx` calls the backend auth endpoints (`src/lib/auth/`) and stores the session client-side.
- Mutual NDA Creator: `NdaCreatorPage.tsx` + `NDAChatPanel.tsx` drive the Mutual NDA fields entirely through a chat conversation (no manual form); `NDADocument.tsx` renders the live preview from the same `NDAFormData` (`src/lib/nda/`), matching the color scheme above.
- PDF export via `src/app/api/generate-pdf/route.ts` (Puppeteer), unchanged by the chat feature.
- Vitest unit tests for `src/lib/auth/` (`api.test.ts`, `session.test.ts`) and `src/lib/nda/chatApi.test.ts`.

**Packaging**: `docker-compose.yml` runs backend (port 8000) and frontend (port 3000) as separate containers, with the backend service reading `OPENROUTER_API_KEY` from the root `.env`; `scripts/start-*` and `scripts/stop-*` exist for Mac/Linux/Windows.

**Not yet implemented**: any catalog document other than the Mutual NDA, and serving the static frontend build from FastAPI (currently two separate containers/ports rather than one).