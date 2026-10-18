# 10 — Prep Calendar (10 days) and 24-Hour Build Schedule

**Version:** 0.1 · **Date:** 2026-10-09
Prep day 1 = the first day after the team confirms this plan. Adjust the dates once O2 (exact clock start) is known.

---

## 1. Prep calendar — content, data, designs and accounts only (no code)

| Day | Focus | Tasks | Owner | Done when |
|---|---|---|---|---|
| **1** | Rules, name, accounts | Written confirmation from organizers (prep scope, AI tools, design docs) · record clock start · confirm app name (search, domain, Play Store) · create accounts/projects for hosting, DB, providers · verify Gemini API quota separate from Pro · check provider data-use terms (O6) | Lead | Written replies saved; accounts ready |
| **1–3** | Official sources | Confirm official URLs (doc 08 §2) · download and store official texts · identify scanned-only documents | Dev C | Source list with dates; raw files stored |
| **1–3** | Helplines | Verify every number and its hours on official sites; screenshots; second-person re-check; fill `helplines.json` draft | Dev C + Lead | All entries have status + date |
| **2–4** | English playbooks | Draft 6 masters from the official text with law cards; fill authoring template | Dev C + Lead | 6 drafts pass quality checklist (doc 09 §9) |
| **2–3** | Advocate | Book the review slot (day 5 or 6); send heads-up | Dev C | Date confirmed |
| **3** | Name and brand | Final name; icon set; colour tokens; spoken-name test in all 3 languages | Dev B | Name/icon decided |
| **4** | Send drafts | Send English masters and trap questions to the advocate | Dev C | Delivered |
| **3–5** | Cleaning corpus | Clean text by Act, split by section on paper/spreadsheet, check counts vs table of contents; build mapping-table rows | Dev C (+ Lead spot check) | Counts match |
| **5–6** | **Advocate review** | 45-minute call; fix changes; written approval per playbook | Dev C + Lead | Sign-off table (doc 08 §13) filled |
| **6–8** | Translations | Hindi and Marathi texts, glossary, back-translation, read-aloud, safety copy | Dev B + Dev C + Lead | Sign-off readers confirm |
| **6–8** | UX content | UI strings in 3 languages; disclaimer copy; consent notice copy; error messages | Dev B | Key parity achieved on paper |
| **7–8** | Eval set | 40 questions with expected sections/refusals; advocate adds 10 traps; safety phrasings | Lead + Dev B | 40 cases stored in a content file |
| **7–8** | Wireframes | Paper/Figma wireframes for 6 screens; test with 3 people on paper (can they find the playbook without reading?) | Dev B | Findings recorded; layout fixed |
| **8–9** | Pitch | Deck, demo script (doc 11), judge Q&A answers; rehearse once | Lead | Deck ready |
| **9** | Environments | Empty deploy targets (web, API, DB with pgvector enabled); secrets stored; no application code | Lead | Targets reachable |
| **9** | Demo kit | Demo phone chosen and fixed; hotspot; second SIM; power banks; cables; speaker; laptop | Dev C | Kit packed |
| **10** | Freeze and rest | Content freeze (version recorded); final read-through; re-verify helplines; rehearse pitch ×2; sleep | All | Content frozen; everyone rested |

**Dependencies:** advocate sign-off (day 5–6) → translations start from the *approved* English; audio generation (during the build) only from final text.

## 2. 24-hour build schedule

| Hours | Lead | Dev B | Dev C |
|---|---|---|---|
| **H0–1** | Repo + CI (C01, C02); start hosting (C06) | Next.js + PWA scaffold (C03) | API scaffold (C04) + DB (C05) |
| **H1–3** | Embeddings (C09); STT test at **H2** (C13); deploy hello-world | Language tiles (C10); home screen start | Ingestion (C07); commit content files (C08) |
| **H3–4** | Safety router + routing (C12 with Dev C); provider interface (C14) | Home screen (C11) | Playbooks/helplines endpoints (C17) |
| **H4–8** | Guard (C16, PR), provider fallback (C15), triage API (C18) | Triage flow (C19), playbook screen (C20) | Review guard (C16); support C17; start eval harness |
| **H8** | **Sync** — tag `v0.1` if skeleton path works | | |
| **H8–12** | `/ask` (C22); eval runs (C25); voice (C26 with Dev B) | Officer card (C21), Ask UI (C23), footer/a11y (C27) | Eval harness + 40 cases (C24) |
| **H12** | **Sync** — tag `v0.5`; decide whether to start P2 | | |
| **H12–16** | Support offline review; voice go/no-go confirmation; start prod hardening | Audio player (C29), service worker (C30), share-location (C31 if kept) | TTS script and files (C28); watcher (C32) only if core stable |
| **H13–16** | — | **Rest** (Dev B, 3 h; adjust) | — |
| **H16** | **FREEZE** — apply cut rules (§3); tag `v0.9` | | |
| **H15–18** | — | — | **Rest** (Dev C, 3 h) |
| **H16–20** | Keep-warm + demo cache (C35); production deploy (C36); then rest H17–20 | Bug bash (C34), offline test (C37), a11y (C38), usability (C42) | Bug bash; README (C39) |
| **H20–22** | Demo freeze (C40); rehearsals | Fixes (C43) | Backup video and assets (C41) |
| **H22–24** | Go/no-go (doc 07 §8); final deploy (C44); decision log (C45); pitch warm-up | Fixes only | Fixes only; kit check |

*Rest windows overlap with phases where other people cover bug-bash; adjust to the event's rules and to who is actually tired.*

## 3. Freeze rules at H16 (decide, don't debate)

| If … at H16 | Then … |
|---|---|
| Watcher not working end to end | **Cut** (cut 1). Show it as a roadmap slide with the design |
| Extra playbooks not signed off and translated | **Cut** (cut 2). Only the 6 reviewed ones ship |
| Share-location unstable | **Cut** (cut 3). Remove the button |
| Marathi voice accuracy unacceptable (per C13/C26) | **Cut** (cut 4). Marathi: text + audio only |
| Audio incomplete for any language | Ship audio for the languages that are complete; hide buttons elsewhere. Full audio cut only if broken for ≥2 languages (cut 5) |
| Offline failing | **Stop everything else** and fix it. Offline is never cut |
| Guard/refusal failing eval | Do not demo Ask; fix before demo, otherwise show Tier-1 playbooks only |

## 4. Go/no-go checkpoints

| Time | Question | If no |
|---|---|---|
| H2 | Does Marathi/Hindi speech recognition meet the bar? | Mark Marathi voice no-go; continue with hi/en |
| H8 | Does the static path (language → home → playbook) work on the demo phone? | Stop other work until it does |
| H12 | Does `/ask` refuse all 10 out-of-scope questions? | Fix guard/threshold before anything else |
| H16 | Is offline working? | See §3 |
| H20 | Is everything frozen and deployed? | Cut remaining risky features |
| H22 | Go/no-go checklist (doc 07 §8) | Use backup video + offline playbooks for the demo |

## 5. Runbook

**Deploy:** merge to `main` → web auto-deploys; API deploys from the same push; verify `/health`; run the 8-call smoke set; check on the demo phone.
**Rollback:** redeploy the previous git tag (web and API); confirm `/health` and smoke set.
**Provider outage:** switch `DEMO_PIN` to a verified fallback model or rely on cached demo answers; announce in the group chat.
**Cold start suspected:** hit the keep-warm route; if the API is down, present offline playbooks and the backup video.
**Content change after freeze:** only for wrong/unsafe legal content; requires the Lead's approval, re-run CI and affected audio.

## 6. T-minus checklist for the day before the clock

☐ Sleep ☐ Chargers, power banks, hotspot, second SIM ☐ Demo phone updated, fixed, battery saver off ☐ Laptop and spare ☐ Printed copy of this pack's schedule and runbook ☐ Content files on a USB drive and in cloud storage (content is allowed prep) ☐ Account logins ready ☐ Provider quotas checked ☐ Helplines re-verified ☐ Food, water, medicines ☐ Everyone knows the cut order.
