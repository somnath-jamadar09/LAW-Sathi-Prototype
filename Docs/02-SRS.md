# 02 — Software Requirements Specification (SRS)

**Product:** LawSathi · **Version:** 0.1 · **Date:** 2026-10-09
**Conformance language:** "shall" = mandatory for the feature's priority; "should" = desirable.

---

## 1. Introduction

### 1.1 Purpose
Defines testable functional and non-functional requirements for the LawSathi MVP built in 24 hours. Each requirement maps to a feature (F01–F17), tests (doc 07) and commits (doc 06).

### 1.2 Scope
A PWA (Next.js) plus a Python API service, a Postgres + pgvector database, third-party LLM, speech and embedding APIs, and static content (playbooks, helplines, audio). Out of scope: see PRD §4.

### 1.3 Definitions
| Term | Meaning |
|---|---|
| Playbook | Pre-written, advocate-reviewed, fixed-format guide for one situation |
| Chunk | One section (or sub-section) of an official law text with metadata |
| Claim | One statement the LLM proposes, paired with a section ID and an exact quote |
| Guard | Deterministic code that checks every claim's quote exists in the cited chunk |
| Tier 1/2/3 | Verified playbook / From the law / Not confirmed |
| Triage | The ≤3 tap questions that choose a playbook |

### 1.4 Assumptions
- Users have a modern Android Chrome (or iOS Safari) browser; screen width ≥ 360 px.
- Official law text and helpline data are collected and cleaned during prep (content only).
- The advocate reviews English masters only; translations are checked by team members.

---

## 2. Functional requirements

### F01 — Language selection
- F01-R1 The app shall show three large tiles labelled in their own scripts (हिंदी, मराठी, English) on first launch.
- F01-R2 The app shall store the chosen language on the device only and use it on later launches.
- F01-R3 The app shall allow changing language from every screen in ≤2 taps.
- F01-R4 The app should play a short spoken greeting in the chosen language after selection (F09 dependency).
- F01-R5 All user-visible strings shall come from language resource files; no hard-coded text in components.

### F02 — Home and emergency access
- F02-R1 A "Call 112" control shall be pinned at the top of every screen.
- F02-R2 The home screen shall contain a large mic button, a grid of situation icons (picture first, text second), and a language switch.
- F02-R3 Situation icons shall open the corresponding triage (F03) or playbook (F04).
- F02-R4 The home screen shall be usable without login, permissions or onboarding.
- F02-R5 Situations without a reviewed playbook shall not be shown as tiles; they shall be reachable through Ask (F06).

### F03 — Guided triage and safety routing
- F03-R1 Before triage, the screen shall display "what to do right now" (generic safety instructions + 112) so help is visible first.
- F03-R2 Triage shall ask at most 3 questions, each with 2–4 large icon buttons and an optional spoken prompt.
- F03-R3 Free-text or voice input shall be classified into one situation, or "unknown", by the API (`/triage`).
- F03-R4 A **safety router** shall run before any LLM call. If the input indicates immediate danger, self-harm, child abuse or sexual assault, the app shall show fixed content with 112 and the relevant national helplines (see doc 13) and shall not generate free-form text.
- F03-R5 If classification confidence is below threshold, the app shall show the situation grid instead of guessing.
- F03-R6 Triage shall work without the LLM for icon taps (static routing table).

### F04 — Verified playbooks
- F04-R1 The app shall provide six playbooks in English, Hindi and Marathi using the fixed format in doc 09 (do now / who to call / what the law says / what to avoid / what happens next).
- F04-R2 Every legal statement in a playbook shall carry a `source_ref` (Act, section ID, source URL, verified date).
- F04-R3 Playbooks shall be served from static JSON, never generated at request time.
- F04-R4 A playbook shall display ✅ Verified only if `reviewed = true`, with reviewer name/role and date.
- F04-R5 Each playbook shall render fully offline (F10).
- F04-R6 Each playbook screen shall show tap-to-call buttons using `tel:` links for relevant helplines.

### F05 — Show-to-officer card
- F05-R1 A single action on every playbook shall open a full-screen, high-contrast card showing: situation title, Act + section, verbatim law text (original language of the law), plain-language line in the user's language, and the app's disclaimer.
- F05-R2 The card shall work offline and be readable at arm's length (≥ 20 px body text).

### F06 — Grounded Q&A (Tier 2)
- F06-R1 The app shall accept a question by text or voice and return an answer object (doc 05 §4.4).
- F06-R2 The API shall retrieve top-k chunks from the corpus using the English form of the query (translated if the user wrote in Hindi/Marathi).
- F06-R3 The answer shall display, first, the verbatim quotes with Act and section; then a plain-language summary composed only from verified claims.
- F06-R4 Each displayed quote shall link to the official source URL and show the "last verified" date.
- F06-R5 Follow-up questions shall use conversation history held **on the client** and sent with each request; the server shall not store it.
- F06-R6 If the query uses old section names (e.g. "IPC 354"), the system shall map them to the current BNS provision using the mapping table and state the mapping.

### F07 — Grounding guard and refusal (Tier 3)
- F07-R1 The model shall be required to return structured output: a list of claims, each with `section_id` and an exact `quote`.
- F07-R2 The guard shall accept a claim only if the normalised quote occurs verbatim inside the cited retrieved chunk (whitespace and Unicode normalisation only; no fuzzy matching).
- F07-R3 Claims failing verification shall be dropped. If no claim survives, or best retrieval score is below threshold, the API shall return `tier = 3`.
- F07-R4 Tier-3 responses shall contain no legal assertion; they shall show "I can't confirm this from the law text" and the relevant helplines.
- F07-R5 The plain-language summary shall be generated from verified claims only and shall not contain section numbers, penalties, time limits or amounts that are absent from the verified quotes (post-check by regular expression for numbers and section references).
- F07-R6 Each guard decision (accepted/rejected claims, scores) shall be logged without the user's text (counts and IDs only).

### F08 — Voice input
- F08-R1 The mic button shall record audio in the browser and send it to `/stt` with the language hint.
- F08-R2 The recorded audio shall not be stored by LawSathi; the app shall show a one-time notice that audio is processed by a third-party speech service (doc 13).
- F08-R3 The transcript shall be shown to the user and be editable before being used.
- F08-R4 If speech recognition fails or is unavailable, the app shall fall back to typing and icons.
- F08-R5 Supported languages: Hindi and English (P1); Marathi (P1, first to be cut — see go/no-go in doc 10).

### F09 — Audio playback
- F09-R1 Every playbook step shall have a pre-generated audio file per language, produced from the *checked* text.
- F09-R2 Audio shall start only on user tap (browser autoplay rules) and shall show a visible progress indicator.
- F09-R3 Audio files shall be cached for offline use (F10).
- F09-R4 Helpline numbers read aloud shall be spoken digit by digit.

### F10 — Offline PWA
- F10-R1 The app shall be installable (manifest, icons, standalone display).
- F10-R2 A service worker shall pre-cache: app shell, language files, all playbook JSON, helplines JSON, icons, and audio files (precache budget ≤ 15 MB; measure).
- F10-R3 When offline, the app shall show an "Offline — showing saved guidance" banner and disable only Ask and Voice features, with an explanation.
- F10-R4 Cached content shall carry a visible "content last updated" date.
- F10-R5 The service worker shall update cached content when online without blocking the UI.

### F11 — Share-my-location (P2)
- F11-R1 On tap, the app shall request device location once, build a map link and open the SMS or WhatsApp composer with a prefilled message to a contact the user chooses.
- F11-R2 The app shall not store or transmit location to LawSathi servers.
- F11-R3 If permission is denied, the app shall explain how to share manually.

### F12 — Freshness watcher and admin review (P2)
- F12-R1 A scheduled job shall fetch 3–5 configured official URLs, normalise the text and compute a hash.
- F12-R2 On hash change, the job shall create a `pending_change` record containing old/new hash, URL, time and a text diff.
- F12-R3 A password-protected admin page shall list pending changes; a human shall approve or reject; **no change reaches the corpus automatically**.
- F12-R4 Every answer shall display "Last verified: <date>" for each cited source.

### F13 — LLM provider pool
- F13-R1 A single interface shall wrap every provider: generate with schema, embed, and (separately) speech functions.
- F13-R2 Only models in the **eligibility list** (those that passed the eval at 100% on refusals/traps and the structured-output check) shall be selectable.
- F13-R3 Selection shall use a running average of observed latency; it shall not probe all providers on every request.
- F13-R4 On timeout, 429 or malformed output, the pool shall fall back to the next eligible model.
- F13-R5 A `DEMO_PIN` setting shall force one model for the demo.
- F13-R6 Several keys from the *same* provider shall not be rotated to bypass rate limits.

### F14 — Helplines directory
- F14-R1 All helplines shall live in one JSON file with: id, display name per language, number, hours (as officially stated), purpose, source URL, verified date, status (`verified` / `conflicting` / `unverified`).
- F14-R2 No helpline number shall appear in code, playbook text or model output except via this file.
- F14-R3 Entries with status other than `verified` shall be hidden from the UI or show their uncertainty (e.g. hours).

### F15 — Ingestion pipeline
- F15-R1 The pipeline shall load official law text into the database one section per chunk with: act, section number, heading, chapter, text, language, source URL, retrieved date, content hash.
- F15-R2 The pipeline shall report counts per Act and flag chunks with empty text, duplicate IDs or unusually short/long length.
- F15-R3 Re-running the pipeline with unchanged input shall create no duplicates.
- F15-R4 One fixed embedding model shall be used for the whole corpus; its identifier and vector size shall be recorded in configuration.

### F16 — Evaluation harness
- F16-R1 A runner shall execute the evaluation set against any provider/model and output a report: pass/fail per case and per category.
- F16-R2 Categories: in-scope (20), out-of-scope (10), traps (10), with expected section IDs or expected refusal.
- F16-R3 The runner shall be callable before every deploy and produce a non-zero result if refusal/trap pass rate < 100%.

### F17 — Labels and disclaimers
- F17-R1 Tier badges (✅ / 📖 / ⚠️) shall be rendered by one shared component driven only by the API `tier` and `reviewed` fields.
- F17-R2 Every screen shall show "General legal information, not legal advice. In danger? Call 112."
- F17-R3 Disclaimers shall be present in all three languages.

---

## 3. Non-functional requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Performance | Opening a cached playbook ≤ 1 s on the demo phone; time from app launch to first instruction ≤ 10 s |
| NFR-02 | Performance | `/triage` p95 ≤ 4 s; `/ask` p95 ≤ 8 s (measured on mobile data) |
| NFR-03 | Availability | API shall not cold-start during demo (always-on instance or keep-warm) |
| NFR-04 | Offline | Everything in F04, F05, F14 and F09 audio works with no network |
| NFR-05 | Accessibility | Touch targets ≥ 48 px; base font ≥ 18 px; contrast WCAG AA; usable at 200% text; labels for screen readers; no information by colour alone |
| NFR-06 | Usability | A first-time user shall reach a playbook in ≤3 taps; no mandatory typing |
| NFR-07 | Compatibility | Android Chrome (current and previous major), iOS Safari; 360×640 up to desktop |
| NFR-08 | Localization | UI, playbooks and disclaimers in en/hi/mr; numbers and helpline names unchanged across languages |
| NFR-09 | Privacy | No personal data stored; no query text in logs; location never sent to our servers |
| NFR-10 | Security | Secrets only in server environment; CORS allow-list; rate limiting per IP; admin route behind a secret; input length limits |
| NFR-11 | Reliability | Provider failure shall degrade to cached playbooks and Tier-3 refusals, never to unguarded output |
| NFR-12 | Maintainability | Content (playbooks, helplines, strings) separated from code; one config file per environment |
| NFR-13 | Observability | Structured logs with request ID, route, tier, latency, provider, guard counts; no user text |
| NFR-14 | Cost | Measure and report cost per 1,000 `/ask` requests for the pinned model |

## 4. External interfaces

| Interface | Direction | Notes |
|---|---|---|
| LLM provider(s) (Gemini API; OpenRouter models) | API → provider | Structured output; keys in env; per-model eligibility |
| Embedding model (one fixed model) | API → provider | Same model for corpus and queries; pinned ID recorded |
| Speech-to-text | API → provider | Evaluated for hi/mr/en at H2; provider chosen by test |
| Text-to-speech | Build-time script → provider | Output stored as static audio |
| Postgres + pgvector (managed) | API ↔ DB | Corpus, playbooks metadata, pending changes, eval results |
| Static hosting / CDN | Web ↔ browser | Playbook JSON, audio, icons |
| Browser APIs | Web | MediaRecorder, Service Worker, Cache Storage, Geolocation (F11), `tel:`, `sms:`, share links |

## 5. Data requirements (summary — details in doc 03 §6 and doc 05)

- Corpus chunk, playbook, helpline, pending change, evaluation case/run.
- **No** user table, session table or query log.
- Content updated by editing files in the repository (playbooks, helplines, strings) or via the approved ingestion pipeline (corpus).

## 6. Constraints and dependencies

- 24-hour build window; no pre-written code.
- Dependence on third-party API quotas; mitigated by pool, caching of demo answers and offline playbooks.
- Dependence on the advocate's sign-off for ✅ badges (target prep day 5–6).

## 7. Acceptance and traceability

A feature is **accepted** when: (1) all its "shall" requirements pass the tests listed in doc 07 on the demo phone, (2) it is merged to `main` and deployed, (3) the commit gate in doc 06 is green.

| Feature | Tests (doc 07) | Commits (doc 06) |
|---|---|---|
| F01 | F01-T1…T4 | C03, C10 |
| F02 | F02-T1…T4 | C11 |
| F03 | F03-T1…T6 | C12, C18, C19 |
| F04 | F04-T1…T6 | C08, C17, C20 |
| F05 | F05-T1…T3 | C21 |
| F06 | F06-T1…T7 | C22, C23 |
| F07 | F07-T1…T8 | C16 |
| F08 | F08-T1…T5 | C26 |
| F09 | F09-T1…T4 | C28, C29 |
| F10 | F10-T1…T6 | C30, C37 |
| F11 | F11-T1…T3 | C31 |
| F12 | F12-T1…T4 | C32 |
| F13 | F13-T1…T6 | C14, C15, C25 |
| F14 | F14-T1…T3 | C08, C17 |
| F15 | F15-T1…T4 | C07, C09 |
| F16 | F16-T1…T3 | C24, C25 |
| F17 | F17-T1…T3 | C23, C27 |
