# 04 — Team Roles and Working Agreements

**Version:** 0.1 · **Date:** 2026-10-09
Replace the placeholders in `[brackets]` with real names on prep day 1.

---

## 1. Team

| Role | Person | Strengths | Primary ownership |
|---|---|---|---|
| **Lead — AI/ML + Cloud + DevOps + Pitch** | [Lead] | AI/ML, cloud | Retrieval, guard, provider pool, deployments, secrets, release, pitch |
| **Frontend (Dev B)** | [Dev B] | Full-stack | PWA UI, i18n, accessibility, offline, audio player |
| **Data/Backend (Dev C)** | [Dev C] | Full-stack | Database, ingestion, playbook/helpline endpoints, TTS script, eval harness, watcher |
| **Dev D (unavailable / partial)** | [Dev D] | Full-stack, DevOps | **Duties absorbed by Lead** — see §3. Any hours Dev D can give go to the "optional help" list |
| **Domain reviewer (external)** | [Advocate, teammate's father] | Criminal law | Reviews English playbooks and trap questions; signs off ✅ |

All team members read and write Marathi, Hindi and English. Each language still gets one named *sign-off reader* so it is nobody's job by default:

| Language | Sign-off reader | Back-up |
|---|---|---|
| English (master) | [Lead] | [Dev C] |
| Hindi | [Dev C] | [Dev B] |
| Marathi | [Dev B] | [Lead] |

## 2. Ownership matrix (R = does the work, A = accountable, C = consulted, I = informed)

| Area | Lead | Dev B | Dev C | Advocate |
|---|---|---|---|---|
| Scope, cut decisions, release | A/R | C | C | I |
| Playbook content (English master) | A | C | R | **C (reviews)** |
| Translations hi/mr + back-translation checks | C | R | R | I |
| Helplines JSON + verification | A | I | R | C |
| Ingestion of official texts | C | I | A/R | I |
| Embeddings, retrieval | A/R | I | C | I |
| Guard + refusal | A/R | I | C (code review) | I |
| Provider pool + eligibility | A/R | I | C | I |
| Triage + safety router | A/R | C (UI) | C | C (phrase list) |
| Web UI, PWA, offline | C | A/R | I | I |
| Audio (TTS generation) | C | R (player) | A/R (script) | I |
| Voice input | A/R | R (mic UI) | I | I |
| Eval harness + test set | R (runs) | I | A/R (harness) | C (traps) |
| Watcher + admin (P2) | C | C (admin UI) | A/R | I |
| Deployment, secrets, CI | A/R | C | C | I |
| Demo, pitch, backup video | A/R | C | R (video, screenshots) | I |
| Risk log, decision log | A/R | C | C | I |

## 3. Dev D's duties and how they are absorbed

| Dev D's original duty | Who takes it | How the load is controlled |
|---|---|---|
| Deployments, secrets, CI | Lead | Done in prep (accounts, empty deploy targets) + **C01–C06 in the first hour**; every later deploy is "merge to main" |
| Audio cache | Dev C (script) | Script runs once per content freeze |
| Demo phone setup, backup video | Dev C / Lead | Phone setup in prep day 9; video recorded at H21 from a frozen build |
| Pitch deck | Lead (prep days 8–9) | Deck is content, built before the clock |
| Test running | Dev B/Dev C run feature tests; Lead runs eval | Test gates in doc 07 per feature |

**Optional help if Dev D is available** (small, independent, no code dependence): proofreading hi/mr text, running test checklists on the demo phone, packing the demo kit, timing rehearsals, recording the backup video.

**Load warning:** the Lead carries the guard, provider pool, retrieval, triage, deployments and the pitch. Mitigations: (1) prepare everything non-code in the prep window, (2) pair-review the guard with Dev C, (3) pair on voice with Dev B, (4) the Lead does **not** own UI polish or the watcher, (5) the Lead sleeps in the planned slot (§6).

## 4. Working agreements

### 4.1 Git and review
- Trunk-based: `main` is always deployable.
- Branch names: `feat/<id>-short-name`, `fix/<id>-short-name`, `chore/<id>-short-name`; one branch per commit ID in doc 06, merged within ~1 hour.
- Commit message format: `type(scope): summary [C##]` with types `feat`, `fix`, `chore`, `test`, `docs`, `perf`.
- **Small commits, pushed at least once per hour per person** (also visible evidence that the work happened inside the 24 hours).
- Pull request required for: guard, provider pool, safety router, offline/service worker. One reviewer (named in doc 06). Everything else may merge directly if tests pass.
- After H16: only `fix:` and `docs:` commits; PR + reviewer for every change.
- Never commit secrets. `.env.example` lists names only.

### 4.2 Definition of Ready (before starting a commit)
- Inputs available (content, schema, API contract in doc 05).
- Acceptance tests identified (doc 07).

### 4.3 Definition of Done (per commit)
1. Code merged to `main` with the commit message format.
2. Tests listed in the commit's *gate* column pass.
3. Deployed to the preview/production environment and checked on the demo phone when UI-visible.
4. Docs updated if a contract changed (doc 05) or a decision changed (doc 12).

### 4.4 Communication
- One chat group for coordination; one shared board (doc 06 table is the source of truth).
- **Sync checkpoints:** H4, H8, H12, H16 (freeze decision), H20, H22 — 5 minutes each, stand-up style: done / next / blocked.
- Blocked >20 minutes → say so in the group; do not stay silent.
- Decisions that change scope are made by the Lead and logged in doc 12.

### 4.5 Pairing for risky parts (no single point of failure)
| Area | Owner | Second person |
|---|---|---|
| Guard | Lead | Dev C |
| Provider pool | Lead | Dev C |
| Voice input | Lead | Dev B |
| Offline/service worker | Dev B | Lead |
| Ingestion | Dev C | Lead |
| TTS/audio | Dev C | Dev B |

### 4.6 Escalation and cut rules
Cut order (agreed): **watcher → extra playbooks → share-location → Marathi voice → audio → offline is never cut.** At H16 the Lead applies the freeze rules in doc 10 §3.

## 5. Prep-period responsibilities (10 days)

| Area | Owner |
|---|---|
| Written confirmation from organizers | Lead |
| Advocate scheduling | Dev C (via teammate) |
| Official text collection + cleaning | Dev C |
| Helpline verification | Dev C, Lead cross-check |
| Draft English playbooks | Dev C + Lead |
| Hindi translation + checks | Dev C (reader), Dev B |
| Marathi translation + checks | Dev B (reader), Lead |
| Evaluation set (40 questions) | Lead + Dev B |
| Wireframes, icon set, UX copy | Dev B |
| Pitch deck | Lead |
| Accounts, keys, empty deploy targets | Lead |
| Demo kit (phone, hotspot, SIM, power bank) | Dev C |

## 6. Rest plan (suggested)

| Person | Rest window | Notes |
|---|---|---|
| Dev B | H13–H16 (3 h) | After offline groundwork is in, before the H16 freeze |
| Dev C | H15–H18 (3 h) | After audio generation is complete |
| Lead | H17–H20 (3 h) | After H16 freeze decision and production deploy; Dev B/C cover bug-bash |

Adjust to the event's rules. No one works the final two hours without having slept or rested.

## 7. Bus-factor table

| Critical item | If the owner is blocked | Backup |
|---|---|---|
| Guard | Dev C reviews/continues from the doc 03 §5.2 spec and unit tests | Dev C |
| Deploys | Dev C has all access and a runbook (doc 10) | Dev C |
| Content | Content is in the repo; any member can edit by schema (doc 09) | Anyone |
| Demo | Backup video + cached answers + offline playbooks | Dev C presents if the Lead cannot |
