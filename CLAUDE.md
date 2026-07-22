# Prelegal Project
## Overview

This is a Saas product to allaow usaers to draft legal agreemants based on templates in the templates directory. The users can carry an AI chat in order to establish what document they want and how to fill in the fields. The available documents are covered in the catalog.json file in the project root,included here:
@catalog.json
V1 supports all 11 documents in catalog.json via a generic chat-driven engine; see Implementation Status below for what has been built so far.
## Development Process

when instructed to build a feature:
1. Use your Atlassian tools to read the feature instructions from Jira
1. Develop the feature - do not skip and step from the feature-dev 7 step process
1. Thoroughly tes the feature with unit tests and integeration tests and fix any issues
1. Submit a PR using your github tools

## Ai Design

When writing code to make calls to LLMs, use your Crebas skill to use LiteLLM via OpoenRouter to the openai/gpt-oss-120b model with Cerebas as the inference provider. You should use structured Outputs so that you can interpret the results and populate fiedls in the legal document.

(The free openai/gpt-oss-20b:free model was tried first but proved unreliable at following the structured-output contract - see Implementation Status. gpt-oss-120b is not a free-tier model but is far more reliable and still runs on Cerebras.)

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

## Implementation Status (as of 2026-07-22)

**Backend** (`backend/`, FastAPI + uv, Python >=3.12):
- SQLite database wiped and recreated on every app startup (`app/db.py`), single `users` table.
- `/api/auth/signup` and `/api/auth/signin` (`app/auth.py`) — fake/passwordless login, matched by email only.
- `app/documents/` — the generic multi-document engine (replaces the old NDA-only `nda_chat.py`/`llm.py`, now deleted):
  - `registry.py` defines a hand-authored `FieldSpec` list per catalog document (~150 fields total across all 11), reverse-engineered from each template's Standard Terms body since only the Mutual NDA ships an actual Cover Page template — the others reference an external Key Terms/Cover Page/SOW/Order Form document this repo doesn't have. Each field is classified `DEFINED_TERM` (a role like Customer/Provider that stays literal in the body, only mapped to its real value on a generated summary table), `SUBSTITUTED` (its matching template span gets replaced with the real value everywhere it appears), or `SUMMARY_ONLY` (no body span at all). Every field always appears on the summary table regardless of role, since exact span wording can't be fully verified without the real Key Terms templates — inline substitution is a best-effort enhancement, not the source of truth.
  - `render.py` loads the real template markdown (via the `markdown` library) and does the substitution — this is genuinely new: the old NDA renderer hand-transcribed the template into TypeScript rather than parsing the real file.
  - `chat.py` + `router.py`: one `POST /api/documents/chat` endpoint, two modes. With no `docId` yet, a small fixed schema figures out (conversationally) which catalog document the user wants, or explains if it's unsupported and suggests the closest match. Once a `docId` is set, a per-document Pydantic schema is built at runtime (`pydantic.create_model`) from that document's `FieldSpec`s, and the model returns the complete field set every turn; the backend merges in only the non-empty values the model actually returned, so a field it forgets to re-mention doesn't get wiped. `GET /api/documents` lists the catalog; `POST /api/documents/{id}/render` returns the rendered HTML (used by the PDF route). All V1 simplifications: single-stage flows (no repeatable Order Form/SOW), list-shaped fields (subprocessors, claim categories) are free text, no cross-document field reuse (e.g. SLA re-asks for Customer/Provider rather than pulling from an existing CSA).
  - Model: `openai/gpt-oss-120b` via LiteLLM/OpenRouter, pinned to Cerebras (see AI Design above for why, over the free 20b model). `litellm` is pinned to `1.70.0` (not latest) because newer releases bundle a Rust extension that failed to build on this machine (no MSVC/Rust toolchain) — re-evaluate if that toolchain becomes available. Retries up to 3 times on malformed JSON or provider errors before a clean `502`.
  - `templates.py` resolves the root `templates/` directory via `PRELEGAL_TEMPLATES_DIR` (mirrors `PRELEGAL_DB_PATH`'s pattern), defaulting to a path relative to this file for local dev; Docker sets it explicitly since the backend's build context changed from `./backend` to the repo root so `templates/` can be copied into the image.
- `/api/health` endpoint. CORS open to `http://localhost:3000`.
- Tests: `test_auth.py`, `test_documents_render.py`, `test_documents_chat.py`, `test_documents_field_merge.py`.

**Frontend** (`frontend/`, Next.js 16 + React 19 + Tailwind 4):
- `LoginScreen.tsx` calls the backend auth endpoints (`src/lib/auth/`) and stores the session client-side.
- `DocumentCreatorPage.tsx` + `DocumentChatPanel.tsx` (replacing the old NDA-only `NdaCreatorPage.tsx`/`NDAChatPanel.tsx`/`NDAForm.tsx`, now deleted) drive any catalog document through one conversational chat — no per-document UI code. `DocumentPreview.tsx` renders the HTML the backend returns each turn. A "start over" action resets `docId`/field values and remounts the chat panel if the user wants a different document. `src/lib/nda/` is gone entirely in favor of `src/lib/documents/` (generic `ChatMessage`/`DocumentChatReply` types + API client) and a shared `src/lib/postJson.ts` helper.
- PDF export via `src/app/api/generate-pdf/route.ts` (Puppeteer) — now calls the backend's render endpoint server-side via `BACKEND_INTERNAL_URL` (the frontend container's own `NEXT_PUBLIC_API_BASE_URL` points at `localhost`, which only works for browser-side calls, not container-to-container ones).
- Vitest unit tests for `src/lib/auth/` and `src/lib/documents/api.test.ts`.

**Packaging**: `docker-compose.yml` — backend now builds from the repo root (`context: ., dockerfile: backend/Dockerfile`) so `templates/` can be copied in, with `PRELEGAL_TEMPLATES_DIR` and `OPENROUTER_API_KEY` (from root `.env`) set; frontend gets `BACKEND_INTERNAL_URL` for its server-side render calls. `scripts/start-*`/`stop-*` exist for Mac/Linux/Windows.

**Known limitations**: single-stage flows only (no repeatable Order Form/SOW/multi-SOW support), list-shaped fields collapsed to free text, no cross-document field reuse, and larger documents (~20 fields, e.g. Software License) can occasionally miss a field or two in one combined chat message — recoverable by the user restating it on the next turn, per the field-merge safeguard above. Serving the static frontend build from FastAPI (one container instead of two) also remains undone.