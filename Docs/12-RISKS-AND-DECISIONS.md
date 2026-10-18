# 12 — Risk Register and Decision Log

**Version:** 0.1 · **Date:** 2026-10-09 · **Owner:** Lead
Update this file whenever a risk changes or a decision is made. Likelihood (L) and Impact (I): H/M/L.

---

## 1. Risk register

| ID | Risk | L | I | Mitigation | Owner | Trigger / contingency |
|---|---|---|---|---|---|---|
| R01 | Model produces a wrong or ungrounded legal statement | M | H | Exact-quote guard; refusal; summary post-check; eval gating; only eligible models; Tier-1 playbooks are static | Lead | Any trap-case failure → model removed from pool; demo uses only playbooks if unresolved |
| R02 | Advocate review slips or is incomplete | M | H | Book day 5–6; send drafts day 4; written sign-off per playbook; ✅ only on signed playbooks | Dev C | If unsigned at H0: show "From the law" label on that playbook; never show ✅ |
| R03 | Marathi/Hindi speech recognition too weak | M | M | Test at H2 (C13); fall back to icons/typing; Marathi voice cut 4 | Lead | Mark no-go; hide mic for that language |
| R04 | Provider rate limits or outage during demo | M | H | Provider pool with fallback; pinned model; cached demo answers; offline playbooks | Lead | Switch pin; use cached answers/backup video |
| R05 | Hosting cold start or network failure at venue | M | H | Always-on API or keep-warm; hotspot + second SIM; offline mode; backup video | Lead/Dev C | Present offline flow; play backup |
| R06 | Rule violation (pre-built code, AI tools not allowed) | L | H | Written confirmation (O1); repo starts empty; docs contain no executable code; hourly commits | Lead | Ask organizers immediately; adjust process |
| R07 | Name collision: "LawSathi" resembles existing products (a practice-management platform for advocates and at least one similar citizen-facing project name) | H | M | Owner chose the name and accepted the risk; keep `APP_NAME` configurable; state clearly in pitch that LawSathi is for citizens in emergencies; don't copy others' wording/branding | Team | If organizers/judges object → rename via config and assets |
| R08 | Legal text outdated or misextracted | M | H | Official sources only; counts vs table of contents; spot checks; number checks; "last verified" dates | Dev C | Remove affected section from corpus; Tier 3 until fixed |
| R09 | Helpline number or hours wrong | M | H | Verify on official sites; status field; re-verify on demo morning; don't claim 24×7 unless official | Dev C | Hide entry until verified |
| R10 | Lead overload (guard, pool, retrieval, triage, deploys, pitch) | H | H | Prep non-code work; pair on guard/voice; cut order; Dev C owns deploy backup; scheduled rest | Lead | Hand UI/watcher/audio fully to Dev B/C; cut P2 |
| R11 | Scraping blocked or pages change structure (Firecrawl or plain fetch) | M | L | Test 3–5 URLs on day 1; plain fetch as alternative; watcher is P2 | Dev C | Cut watcher; show design on roadmap slide |
| R12 | Copyright/licence concerns about texts | L | M | Official government texts only; no commentary; cite source | Dev C | Remove disputed text |
| R13 | Misuse or over-reliance (user treats app as lawyer) | M | M | Disclaimers; refuses personal-case advice; points to 112/legal aid | Lead | Strengthen copy |
| R14 | Provider data-use terms (free tiers may use inputs to improve models) | M | M | Check terms (O6); disclose third-party processing; avoid sending personal identifiers; use paid tier if needed | Lead | Switch tier/provider for demo |
| R15 | Safety-critical queries (self-harm, child abuse, assault) mishandled | L | H | Safety router before any model; fixed reviewed copy; advocate + native readers review phrases | Lead | Disable free-form Ask for these cues |
| R16 | Embedding/retrieval misses the right section | M | M | Section-per-chunk; threshold tuning on eval; keyword boost for exact references | Lead | Lower k/threshold only if refusals stay 100% |
| R17 | Service worker bugs (stale cache, large precache) | M | H | PR review; precache ≤15 MB; version file; offline tests; never cut | Dev B | Reduce audio quality before reducing offline |
| R18 | Team fatigue → errors late | H | M | Rest windows; code freeze at H16; PR for late changes | All | Stop merging after H21 except Sev-1 |
| R19 | Scope creep ("add more") | H | M | Cut order; extras only if signed + translated; Tier-2 covers breadth | Lead | Say no; log the idea for roadmap |
| R20 | Dev D unavailable | H | M | Duties absorbed per doc 04 §3; non-code prep earlier | Lead | Use optional-help list if D appears |

## 2. Decision log (ADRs)

| ID | Decision | Date | Status | Rationale | Alternatives rejected |
|---|---|---|---|---|---|
| ADR-001 | Ship an **installable PWA**; no APK wrapper in the 24 hours | 2026-10-09 | Accepted | No sponsor requirement; PWA gives offline, install, low risk | Capacitor/TWA (time risk) |
| ADR-002 | **One Python service + Next.js**; drop the separate Node backend | 2026-10-09 | Accepted | Fewer runtimes, fewer deploys, faster for 4 people | Node + Python split |
| ADR-003 | **Quote-verification guard** (deterministic) instead of an LLM judge | 2026-10-09 | Accepted | Cannot be wrong in the same way as the model; headline claim | LLM judge; free generation with citations |
| ADR-004 | **Three tiers** and honest labels; ✅ only for advocate-signed playbooks | 2026-10-09 | Accepted | Breadth without false claims; trust signal | Single unlabelled answer type |
| ADR-005 | **Provider pool** with eligibility list, latency-based pick, fallback, demo pin; no multi-key rotation within one provider | 2026-10-09 | Accepted | Speed + resilience without breaking provider terms | Single provider; racing all keys per request |
| ADR-006 | **Stateless** API; history on the client; no query text in logs | 2026-10-09 | Accepted | Privacy and trust for sensitive situations | Server-side sessions |
| ADR-007 | **Retrieve over English law text**; translate queries and display | 2026-10-09 | Accepted | Official text is in English; avoids retrieving over machine-translated law | Index translated law |
| ADR-008 | **Pre-generated static audio** from checked text | 2026-10-09 | Accepted | Offline, low cost, no live TTS failure | Live TTS |
| ADR-009 | **No OCR/document scan in MVP** | 2026-10-09 | Accepted | Privacy design, OCR errors, time | Image/doc scan v1 |
| ADR-010 | **No lawyer marketplace**; link to helplines and legal aid | 2026-10-09 | Accepted | Regulatory and liability complexity | Marketplace |
| ADR-011 | **Official sources only**; no scanned books; no open crawler; watcher is a human-review queue | 2026-10-09 | Accepted | Grounded truth; copyright; accuracy | Crawl-and-auto-update |
| ADR-012 | **Cut order:** watcher → extra playbooks → share-location → Marathi voice → audio; offline never | 2026-10-09 | Accepted | Protects demo-critical path | — |
| ADR-013 | **Working name "LawSathi"** (owner decision); `APP_NAME` configurable | 2026-10-09 | Accepted (risk R07) | Owner choice; low cost to rename | Distinctive alternative names suggested earlier |
| ADR-014 | **No pre-written code**; docs contain no executable code; content/data/designs prepared in 10 days | 2026-10-09 | Accepted (pending O1) | Organizer rule as understood | — |
| ADR-015 | **Helplines**: use 139 for railways; do not use 182 unless officially confirmed; don't claim 24×7 for 15100 | 2026-10-09 | Accepted | Sources conflict / merger reported | Use remembered lists |
| ADR-016 | **Safety router** before any model for danger/self-harm/child abuse/sexual assault | 2026-10-09 | Accepted | Highest-risk inputs must not rely on free generation | LLM-only handling |

## 3. Open decisions

| ID | Decision needed | Due | Owner |
|---|---|---|---|
| D1 | Speech-to-text provider and Marathi voice go/no-go | H2 | Lead |
| D2 | Embedding model ID (pin after checking provider docs) | H2 | Lead |
| D3 | Retrieval threshold and k values | H11 | Lead |
| D4 | Which bonus playbooks (if any) | H12 | Lead |
| D5 | Hosting provider for API (Render/Railway/Cloud Run) | Prep day 9 | Lead |
| D6 | Whether to keep the watcher after H16 | H16 | Lead |

## 4. Change log

| Date | Change | By |
|---|---|---|
| 2026-10-09 | Initial pack created | Lead + assistant |
