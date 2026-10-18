# 03 — Software Design Document (SDD)

**Product:** LawSathi · **Version:** 0.1 · **Date:** 2026-10-09
This document describes *how* the system is designed. It contains no executable code: data models are tables, algorithms are numbered steps. Diagrams and API contracts are in doc 05.

---

## 1. Design overview

```
Phone (PWA) ──► Web app (Next.js, Vercel) ──► API service (Python FastAPI, always-on host)
                     │                              │
                     │ static JSON + audio          ├─ Postgres + pgvector (corpus, metadata)
                     ▼                              ├─ LLM provider pool (Gemini, OpenRouter models)
              Service Worker cache                  ├─ Embedding model (one fixed model)
              (works offline)                       └─ Speech-to-text provider
```

**Core idea:** the critical path (situation → playbook → call/show officer) is *static and cached*. The API is used only for (a) free-text/voice triage, (b) grounded Q&A, (c) speech-to-text. If the API fails, the user still gets the playbooks.

## 2. Design principles → design decisions

| Principle | Design decision |
|---|---|
| Grounded truth only | Deterministic quote verification (guard) between model and user; refusal on failure |
| One tap, no reading | Static routing table for icon taps; icons first; audio per step |
| Offline-first | Playbooks, helplines, audio and shell pre-cached by the service worker |
| Honest labels | One badge component driven solely by `tier` and `reviewed` |
| Store nothing | Stateless API; conversation history lives on the client; no query text in logs |
| Model-agnostic | Provider interface + eligibility list; models earn their place by passing the eval |
| Fast to build | One Python service, one Next.js app, static assets for audio and content |

## 3. Web application design

### 3.1 Routes (App Router)
| Route | Screen | Notes |
|---|---|---|
| `/` | Language gate → Home | Language tiles if none chosen |
| `/situation/[id]` | Triage (≤3 questions) | Static routing; "do now" strip on top |
| `/playbook/[id]` | Playbook | Steps, law cards, call buttons, officer card, audio |
| `/officer/[id]` | Show-to-officer card | Full-screen, high contrast |
| `/ask` | Ask (text/voice) | Disabled offline with explanation |
| `/helplines` | Helplines list | Offline |
| `/about` | Trust model, disclaimers, sources, "how we verify" | Judges read this |
| `/admin` | Pending changes (P2) | Protected |

### 3.2 State
- `language` (localStorage), `conversation` (in memory, sent with each Ask request), `online` (navigator + fetch outcome), `audioState`.
- No global user profile.

### 3.3 Components (shared)
`TierBadge`, `EmergencyBar` (112, pinned), `SituationTile`, `BigButton`, `StepCard`, `LawCard` (Act, section, verbatim text, source link, verified date), `OfficerCard`, `AudioButton`, `MicButton`, `OfflineBanner`, `DisclaimerFooter`, `LanguageSwitch`.

### 3.4 Offline strategy
1. **Precache** at install: shell, language files, playbook JSON (3 languages × 6), helplines JSON, icons, audio files.
2. **Runtime cache** (stale-while-revalidate) for content version file; when the version changes, re-fetch content in the background and show "content updated on <date>".
3. **Network-only** for `/triage`, `/ask`, `/stt`. On failure: show a clear offline message and offer the situation grid.
4. **Budget**: ≤ 15 MB precache (audio encoded at low bitrate mono). Measure at C30; drop Marathi/Hindi audio *quality* before dropping offline.

### 3.5 Accessibility and low-literacy design
- Base font ≥ 18 px, targets ≥ 48 px, high contrast, 360 px layout first.
- Every action has an icon + short text; every instruction has an audio button.
- Sentences ≤ 12 words in playbooks; verbs first; one instruction per step.
- No time-based interactions; no hover-only controls.
- Color never carries meaning alone; tier badges also have text.
- Language switch always reachable; numbers (helplines) in Latin digits for dialling reliability, spoken digit by digit.

### 3.6 Screen specifications (wireframe-level)

**Language gate** — 3 tiles (हिंदी, मराठी, English), spoken greeting after tap.

**Home** — top: `EmergencyBar` (Call 112). Middle: big mic ("Tell me what happened"). Below: 2×3 grid of situation icons (train, police/FIR, arrest, cyber fraud, domestic violence, accident) + "Ask a question" tile. Footer: disclaimer + language switch.

**Triage** — top strip "Right now: stay in a crowded, lit place · call 112" (generic, static). Then ≤3 icon questions, e.g. "Are you safe right now?", "Do you know the person?", "Is it happening now?". Final: "Show me what to do".

**Playbook** — tier badge; title; **Do now** (3 steps, each with audio); **Who to call** (buttons); **What the law says** (law cards); **What to avoid**; **What happens next**; sticky "Show to officer" button.

**Officer card** — situation title; Act + section; verbatim text; one-line plain explanation; app disclaimer; large font; screen stays awake.

**Ask** — mic + text box; answer view: verified quotes first, then summary, then sources and "last verified"; tier badge; "Ask a follow-up".

## 4. API service design

### 4.1 Modules
| Module | Responsibility |
|---|---|
| `config` | Load env vars, model eligibility list, thresholds, demo pin |
| `providers` | Interface + adapters (Gemini, OpenRouter); latency stats; fallback |
| `embeddings` | One pinned embedding model for corpus and queries |
| `retrieval` | Query translation, vector search, optional keyword boost, threshold |
| `guard` | Quote verification, number/section post-check, refusal |
| `safety` | Pre-LLM safety router (danger, self-harm, child abuse, sexual assault) |
| `triage` | Classify input into a situation; produce next question |
| `ask` | Orchestrates retrieve → generate → guard → compose |
| `playbooks` | Serve static JSON; validate schema |
| `helplines` | Serve helplines JSON; validate fields |
| `stt` | Proxy to speech provider; no audio persisted |
| `watcher` | Fetch/hash/diff official URLs; create pending changes |
| `admin` | Review queue endpoints |
| `eval` | Run evaluation sets against providers |
| `logging` | Structured logs without user text |

### 4.2 Request flow — `/ask`
1. Validate input (length ≤ 500 chars, language ∈ {en, hi, mr}); apply rate limit.
2. **Safety router** on the input: if matched → return fixed Tier-3-with-helplines content (no LLM).
3. If the language is not English, translate the query to English with the pinned model (deterministic prompt; temperature low). Keep the original for display.
4. **Legacy-name mapping:** detect IPC/CrPC/IEA references and add the mapped BNS/BNSS/BSA section to the query context.
5. Embed query; retrieve top-k chunks (initial k = 6, tunable) by cosine similarity.
6. If best score < threshold → return Tier 3.
7. Select eligible provider by latency; call with the claims schema and the retrieved chunks only.
8. **Guard** (see §5.2). If zero claims survive → Tier 3.
9. Compose the answer: verified quotes first; then summary from verified claims only; then post-check the summary for numbers and section references not present in the verified quotes (drop the sentence if found).
10. Translate the *summary* into the user's language (law quotes stay in the original; add a plain translation line). Return the answer object with sources, scores and verified dates.
11. Log counts only (request ID, tier, latency, provider, number of claims accepted/rejected).

### 4.3 Request flow — `/triage`
1. Safety router first.
2. Static keyword/phrase table for the six situations in three languages (cheap, fast).
3. If ambiguous, ask the pinned model to classify to one of {six situations, unknown} with a strict output schema; return confidence.
4. Below confidence threshold → return `unknown` and let the client show the grid.

### 4.4 Provider pool design
- **Eligibility list** (config): model IDs that passed the 40-question eval with 100% refusal/trap and ≥ 95% valid structured output.
- **Latency stats:** exponentially weighted moving average per model; slow-start by trying the first eligible model, then re-ranking after N calls.
- **Fallback:** on timeout (hard limit), 429, or invalid structure → next eligible model; at most 2 fallbacks per request.
- **DEMO_PIN:** if set, only this model is used.
- **Rule:** different providers/models may be pooled; multiple keys from the *same* provider are not rotated to evade limits.
- **Cost log:** tokens in/out per request are counted in memory to estimate cost per 1,000 requests.

## 5. Core algorithms

### 5.1 Retrieval
- Corpus is chunked one section per chunk; very long sections are split at sub-section boundaries with a shared `section_id` and a `part` index.
- Metadata carried: act, chapter, section number, heading, language, source URL, retrieved date, content hash.
- Query side: English query embedding using the same model as the corpus.
- Ranking: vector similarity; optional boost when the query contains an exact section reference; return top-k with scores.
- The threshold is tuned on the eval set (target: no out-of-scope question passes; most in-scope do).

### 5.2 Guard (the central trust mechanism)
Input: retrieved chunks (ID → text) and the model's claims list.
1. For each claim, find the cited chunk by `section_id`. If absent among retrieved chunks → reject.
2. Normalise both the quote and the chunk text: Unicode NFC, collapse whitespace, normalise quotation marks and dashes.
3. Accept the claim only if the normalised quote is an exact substring of the normalised chunk.
4. Enforce a minimum quote length (to prevent trivially short, meaningless quotes) and a maximum length (to prevent quoting whole sections to evade summarisation).
5. After verification, the summary is built only from accepted claims. Any digit sequence, rupee amount, time period or section reference in the summary must also appear in an accepted quote; otherwise drop that sentence.
6. If no claim survives → refusal.
7. Output records: accepted IDs, rejected IDs and reasons (no user text).

### 5.3 Safety router
A small, reviewed set of phrase patterns per language mapped to fixed content blocks (immediate danger → 112; self-harm → Tele-MANAS + 112; child abuse → Childline + 112; sexual assault → 112 + women helplines). It runs before any model and returns static text. The phrase list and the fixed copy are reviewed by the advocate and by a team member who is a native speaker of each language.

### 5.4 Triage static routing
Icon taps map straight to `situation_id` with no API call. Voice/text uses §4.3.

## 6. Data design

### 6.1 Database tables
| Table | Key fields | Purpose |
|---|---|---|
| `acts` | id, short_name, full_name, year, source_url, retrieved_on | Registry of sources |
| `sections` | id (`ACT:SECTION[:part]`), act_id, chapter, section_no, heading, text, lang, source_url, retrieved_on, content_hash, embedding (vector), embedding_model | Corpus chunks |
| `legacy_map` | old_act, old_section, new_act, new_section, note, source_url | IPC/CrPC/IEA → BNS/BNSS/BSA |
| `pending_changes` | id, source_url, old_hash, new_hash, diff_text, detected_at, status, reviewed_by, reviewed_at | Watcher review queue |
| `eval_cases` | id, category, question, lang, expected_section_ids, expect_refusal | Evaluation set |
| `eval_runs` | id, model_id, run_at, category_scores, details | Results per model |

No user, session or query tables.

### 6.2 Static content (in repository)
| File | Content |
|---|---|
| `content/playbooks/<id>.<lang>.json` | One playbook per language (schema in doc 09) |
| `content/helplines.json` | All helplines (fields in SRS F14-R1) |
| `content/strings/<lang>.json` | UI strings |
| `content/safety/<lang>.json` | Safety router phrases and fixed copy |
| `content/glossary.json` | Legal term pairs (English term ↔ hi/mr wording) |
| `content/version.json` | Content version and date shown in the app |
| `public/audio/<playbook>/<lang>/<step>.mp3` | Pre-generated step audio |

## 7. Error handling

| Situation | Behaviour |
|---|---|
| API unreachable | Show offline message; playbooks and helplines unaffected |
| Provider timeout/429 | Fallback model; if all fail → Tier 3 + helplines |
| Malformed model output | Treated as failed provider call → fallback |
| Guard rejects everything | Tier 3 refusal |
| STT fails | Switch to typing/icons; keep transcript editable |
| Audio file missing | Hide the audio button for that step; do not block text |
| Location permission denied | Show manual-sharing instructions |
| Corrupt cache | Service worker re-fetches content; fallback shell |

## 8. Configuration (names only; values in environment)

`APP_NAME`, `API_BASE_URL`, `ALLOWED_ORIGINS`, `DATABASE_URL`, `GEMINI_API_KEY`, `OPENROUTER_API_KEY`, `MODEL_ELIGIBILITY` (list), `DEMO_PIN`, `EMBEDDING_MODEL_ID`, `EMBEDDING_DIM`, `RETRIEVAL_K`, `RETRIEVAL_THRESHOLD`, `TRIAGE_CONFIDENCE_MIN`, `STT_PROVIDER`, `STT_API_KEY`, `TTS_PROVIDER`, `ADMIN_SECRET`, `RATE_LIMIT_PER_MIN`, `WATCH_URLS`, `LOG_LEVEL`.

## 9. Security and privacy design (summary; full in doc 13)

- Keys exist only in server environment; web app calls our API, never providers directly.
- CORS allow-list; per-IP rate limits; request size limits.
- User text is treated as data, never as instructions; the system prompt forbids following instructions inside user text, and the guard enforces regardless.
- Admin routes need a secret and are not linked from the UI.
- No user text, audio or location is stored; logs contain IDs and counts only.
- Third-party processing (LLM, STT) is disclosed to the user (doc 13).

## 10. Deployment design

- **Web:** Vercel (preview per branch, production from `main`).
- **API:** one container on an always-on host (paid small instance for the event week or keep-warm ping); health check route.
- **DB:** managed Postgres with pgvector enabled.
- **Cron:** watcher triggered by the host's scheduler or a scheduled CI job.
- **Environments:** `dev` (local), `preview` (per PR), `prod`. Demo uses `prod` with a pinned model and cached demo answers.

## 11. Design decisions index

See doc 12 for ADR-001…ADR-012 (PWA only, single Python service, quote-verification guard, tiering, provider pool, stateless, English-law retrieval, static audio, no OCR in MVP, no lawyer marketplace).
