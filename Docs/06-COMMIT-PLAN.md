# 06 — Commit Plan: Tasks Assigned per Commit

**Version:** 0.1 · **Date:** 2026-10-09
Owners: **L** = Lead, **B** = Dev B (frontend), **C** = Dev C (data/backend). `H` = hour of the 24-hour clock. Status column is filled during the event: ☐ todo · ◐ in progress · ☑ done · ✂ cut.

---

## 1. Conventions

- Message format: `type(scope): summary [C##]`. Types: `feat`, `fix`, `chore`, `test`, `docs`, `perf`.
- Branch: `feat/c16-guard`, `fix/c34-bugbash-1`, etc. One branch per commit ID unless noted.
- **Gate** = tests from doc 07 that must pass before merge (and, for UI, a check on the demo phone).
- **Reviewer** is required where marked `PR`; otherwise merge when the gate passes.
- Push at least hourly. The commit history is the proof that the build happened inside the clock.
- Content files prepared during prep (playbooks, helplines, strings, eval cases) are committed at H1 as C08; no application code exists before H0.

## 2. Milestone tags

| Tag | When | Meaning |
|---|---|---|
| `v0.1` | ~H6 | Skeleton deployed: language → home → static playbook |
| `v0.5` | ~H12 | Triage + Ask + guard + provider pool working end to end |
| `v0.9` | **H16 (freeze)** | All P0 features working; cut decisions made |
| `v1.0-rc` | H21 | Demo data frozen, rehearsal build |
| `v1.0` | H23 | Final deploy |

## 3. Commits

### Phase A — Foundation (H0–H3)

| ID | Owner | H | Commit | Deliverable | Gate | Status |
|---|---|---|---|---|---|---|
| C01 | L | 0 | `chore(repo): initial structure [C01]` | Repo layout (`web`, `api`, `content`, `docs`, `scripts`), `.gitignore`, `.env.example` (names only), license, README with run notes | Repo opens cleanly on all machines | ☐ |
| C02 | L | 0–1 | `ci: lint, content checks, PR template [C02]` | CI workflow: lint, content schema validation, string-key parity check | CI green on an empty PR | ☐ |
| C03 | B | 0–1 | `feat(web): Next.js scaffold, PWA manifest, theme tokens, i18n skeleton [C03]` | App boots; manifest + icons; language resource loading; theme tokens (font ≥18 px, contrast) | F01-T1 | ☐ |
| C04 | C | 0–1 | `feat(api): FastAPI scaffold, /health, config, CORS, request IDs [C04]` | `/health` returns OK; config loader; structured logging without user text | NFR-13 check | ☐ |
| C05 | C | 1 | `chore(db): provision DB, enable pgvector, migrations, schema v1 [C05]` | Tables per doc 03 §6.1 | F15-T1 (connection + tables) | ☐ |
| C06 | L | 1 | `chore(deploy): deploy web + api hello-world with secrets [C06]` | Production URLs live; secrets set; web can call `/health` | Smoke on demo phone over mobile data | ☐ |
| C07 | C | 1–3 | `feat(ingest): importer for official texts into sections [C07]` | One chunk per section with metadata and hash; counts report; idempotent re-run | F15-T2…T4 | ☐ |
| C08 | C | 1–2 | `content: playbooks, helplines, strings, safety, glossary, eval cases [C08]` | All prepared content files committed; loaders validate schemas | F04-T1, F14-T1…T3; CI schema check | ☐ |
| C09 | L | 2–3 | `feat(embed): embedding job + vector index, model ID recorded [C09]` | All chunks embedded with the pinned model; ID and dimension in config | F15-T4 | ☐ |
| C10 | B | 1–3 | `feat(web): language tiles, remember choice, i18n loading [C10]` | First-launch gate; switch from any screen; spoken-greeting hook (stub) | F01-T1…T4 | ☐ |
| C11 | B | 2–4 | `feat(web): home screen with pinned 112, mic, situation grid [C11]` | Home matches doc 03 §3.6; `EmergencyBar` on every screen | F02-T1…T4 | ☐ |
| C12 | L + C | 3–4 | `feat(safety): safety router and static triage routing [C12]` | Fixed content for danger/self-harm/child abuse/sexual assault; icon-tap routing table | F03-T1…T3 | ☐ |
| C13 | L | 2 | `docs(decisions): speech-to-text test result [C13]` | 10 spoken sentences each in hi/mr/en tested on candidate STT; **go/no-go** for Marathi voice recorded in doc 12 | Result recorded | ☐ |

### Phase B — Core pipeline (H3–H8)

| ID | Owner | H | Commit | Deliverable | Gate | Status |
|---|---|---|---|---|---|---|
| C14 | L | 3–5 | `feat(llm): provider interface + Gemini adapter [C14]` | Structured generation + embeddings through one interface | F13-T1, F13-T2 | ☐ |
| C15 | L | 5–6 | `feat(llm): OpenRouter adapter, latency selection, fallback, DEMO_PIN [C15]` | EWMA latency pick, ≤2 fallbacks, pin | F13-T3…T6 | ☐ |
| C16 | L (reviewer: C) **PR** | 4–8 | `feat(guard): quote verification, summary post-check, refusal [C16]` | Normalised exact-substring check; min/max quote length; number/section post-check; unit tests | F07-T1…T8 | ☐ |
| C17 | C | 3–5 | `feat(api): playbooks and helplines endpoints [C17]` | `/v1/playbooks`, `/v1/helplines`, `/v1/content/version` | F04-T2, F14-T1 | ☐ |
| C18 | L | 6–8 | `feat(api): /triage classification [C18]` | Static phrase table → model classification → confidence | F03-T4…T6 | ☐ |
| C19 | B | 5–8 | `feat(web): triage flow (≤3 big-button questions) [C19]` | "Right now" strip + icon questions + result routing | F03-T1…T6 (UI) | ☐ |
| C20 | B | 5–8 | `feat(web): playbook screen [C20]` | Steps, law cards, call buttons, tier badge (shared component stub) | F04-T3…T6 | ☐ |
| — | all | 8 | **Sync H8** | `v0.1` tag if skeleton path works | — | ☐ |

### Phase C — Q&A, evaluation, voice (H8–H12)

| ID | Owner | H | Commit | Deliverable | Gate | Status |
|---|---|---|---|---|---|---|
| C21 | B | 8–9 | `feat(web): show-to-officer card [C21]` | Full-screen card, ≥20 px text, keep-screen-awake | F05-T1…T3 | ☐ |
| C22 | L | 8–11 | `feat(api): /ask pipeline [C22]` | Retrieve → generate → guard → compose; legacy-name mapping; refusal | F06-T1…T7, F07 | ☐ |
| C23 | B | 8–11 | `feat(web): Ask screen, citations, refusal UI, TierBadge [C23]` | Quotes first, summary after, sources, "last verified"; one `TierBadge` | F06 UI, F17-T1 | ☐ |
| C24 | C | 8–11 | `test(eval): evaluation harness + 40 cases [C24]` | CLI runner; per-category report; exit code on refusal/trap < 100% | F16-T1…T3 | ☐ |
| C25 | L | 11–12 | `test(eval): per-model run, eligibility list, demo pin [C25]` | `MODEL_ELIGIBILITY` set from results; cost per 1,000 recorded | F13-T1, F16 | ☐ |
| C26 | L + B | 9–12 | `feat(voice): /stt route, mic recorder, editable transcript, consent notice [C26]` | Hindi + English first; Marathi per C13 go/no-go | F08-T1…T5 | ☐ |
| C27 | B | 11–12 | `feat(web): disclaimer footer, text sizing, a11y basics [C27]` | Footer on every screen in three languages | F17-T2, F17-T3, NFR-05 | ☐ |
| — | all | 12 | **Sync H12** | `v0.5` tag; decide whether to start P2 work | — | ☐ |

### Phase D — Audio, offline, extras (H12–H16)

| ID | Owner | H | Commit | Deliverable | Gate | Status |
|---|---|---|---|---|---|---|
| C28 | C | 12–14 | `feat(audio): TTS generation script and files [C28]` | One file per step per language from *checked* text; helpline digits spoken singly | F09-T1, F09-T4 | ☐ |
| C29 | B | 13–15 | `feat(web): audio player per step [C29]` | Tap to play, progress, cached | F09-T2, F09-T3 | ☐ |
| C30 | B (reviewer: L) **PR** | 12–15 | `feat(pwa): service worker precache, offline banner, update flow [C30]` | Precache ≤ 15 MB; offline banner; version refresh | F10-T1…T6 | ☐ |
| C31 | B | 15–16 | `feat(web): share-my-location action [C31]` | One-time geolocation → SMS/WhatsApp link; nothing stored | F11-T1…T3 | ☐ ✂? |
| C32 | C | 14–18 | `feat(watcher): fetch, hash, pending changes, admin page [C32]` | Scheduled run; diff; admin approve/reject; "last verified" shown | F12-T1…T4 | ☐ ✂? |
| C33 | C + all | 12–16 | `content: bonus playbooks [C33]` | Extra playbooks ingested only if signed off and translated | F04, F14 | ☐ ✂? |
| — | all | 16 | **FREEZE** `v0.9` | Cut decisions per doc 10 §3 | Doc 07 §8 go/no-go draft | ☐ |

### Phase E — Hardening (H16–H20)

| ID | Owner | H | Commit | Deliverable | Gate | Status |
|---|---|---|---|---|---|---|
| C34 | all | 16–18 | `fix: bug bash round 1 on demo phone [C34]` | Issues from doc 07 §7 checklist | Sev-1/2 closed | ☐ |
| C35 | L | 16–17 | `perf: keep-warm, demo-answer cache [C35]` | No cold start; pre-warmed answers for scripted demo questions | NFR-03 | ☐ |
| C36 | L | 17–18 | `chore(prod): production deploy, env audit, rate limits [C36]` | Secrets audit; rate limiting live; CORS allow-list | NFR-10 | ☐ |
| C37 | B | 17–18 | `test(offline): airplane-mode run on demo phone, results logged [C37]` | Results table in `docs/test-results` | F10-T1…T6 | ☐ |
| C38 | B | 18–19 | `fix(a11y): accessibility pass [C38]` | Contrast, targets, labels, text scaling | NFR-05 | ☐ |
| C39 | C | 19–20 | `docs: README run notes and known limitations [C39]` | Judges' README, architecture picture, honest limitations | Review by L | ☐ |
| C40 | L | 20 | `chore(release): demo data freeze, seeded pending change, v1.0-rc [C40]` | Frozen content, pinned model, seeded watcher example (if C32 kept) | Full eval run | ☐ |

### Phase F — Demo readiness (H20–H24)

| ID | Owner | H | Commit | Deliverable | Gate | Status |
|---|---|---|---|---|---|---|
| C41 | C | 20–22 | `docs(demo): backup video, screenshots, deck export [C41]` | Recorded from the frozen build; stored under `demo/` | Plays on the demo laptop and phone | ☐ |
| C42 | B + C | 17–19 | `test(usability): 3–5 volunteer walkthroughs, findings logged [C42]` | Observation notes; top fixes list | Findings triaged | ☐ |
| C43 | all | 21–23 | `fix: issues from rehearsals [C43]` | Only Sev-1/2; PR required | Rehearsal passes ×3 | ☐ |
| C44 | L | 23 | `chore(release): final deploy v1.0 [C44]` | Tag `v1.0`; production URL checked on mobile data | Doc 07 §8 go/no-go all green | ☐ |
| C45 | L | 23–24 | `docs: decision log and submission notes [C45]` | Final doc 12; links for judges | — | ☐ |

## 4. Rules for the last 8 hours

- After H16: only `fix:`/`docs:`/`chore(release):` commits. Each needs a PR and a named reviewer.
- After H21: only Sev-1 fixes (app unusable, wrong legal content, demo-blocking).
- Never push an untested change to `main` in the last hour. If unsure, do not merge.
- Rollback = redeploy the previous tag. The Lead keeps the tag list in the group chat.

## 5. Dependency map (what blocks what)

```
C01 → C02, C03, C04
C04 → C05 → C07 → C09 → C22
C08 → C17, C20, C28
C14 → C15 → C25
C16 → C22
C12 → C18 → C19
C20 → C21
C22 → C23, C24
C24 → C25
C28 → C29 → C30
C30 → C37
```
