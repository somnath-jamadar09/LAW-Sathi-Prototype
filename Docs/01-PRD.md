# 01 — Product Requirements Document (PRD)

**Product:** LawSathi · **Version:** 0.1 · **Date:** 2026-10-09 · **Owner:** Team Lead

---

## 1. Summary

LawSathi is a mobile-first web app (installable PWA) that gives people in India fast, trustworthy legal guidance in a crisis. A person in trouble — for example being harassed on a train — taps one icon or speaks in Hindi, Marathi or English and immediately sees: **what to do now, which law applies (with the exact text), whom to call, and what to avoid**. The app answers only from official law text and lawyer-reviewed playbooks, refuses when it cannot confirm, and keeps the core guidance available **offline**.

## 2. Problem

- Most people do not know their basic rights or what procedure to follow when something goes wrong (police refuse an FIR, arrest, cyber fraud, harassment, domestic violence, road accident).
- Legal information is written in dense English and organised by Act and section, not by situation.
- People who are scared, in a hurry, or unable to read English cannot search legal text.
- General-purpose chatbots can invent section numbers or advice. In a legal emergency a confident wrong answer can cause real harm.
- Connectivity is unreliable exactly where help is needed (moving trains, rural areas).
- Old IPC/CrPC numbers are still in popular use, although the BNS, BNSS and BSA came into force in July 2024. Search results and model memory mix the two.

## 3. Target users

| Persona | Description | Needs | Design implication |
|---|---|---|---|
| **Sunita, 34** — travels by train for work | Reads Marathi, limited English, uses WhatsApp and voice notes, low-end Android phone, patchy signal | One-tap help, spoken answers, nothing to type | Icon-first home, voice in/out, offline playbooks |
| **Rahul, 24** — just lost money to a UPI scam | Literate, bilingual, panicking, wants the next step now | "What do I do in the next 10 minutes", correct number to call | Situation tile → steps → 1930 call button |
| **Meera, 45** — NGO volunteer / family helper | Helps others understand their rights | Reliable citations she can show to an officer | Section text, "show to officer" card, source links |

Secondary: law students and paralegals (read the sourced text), judges/evaluators (see rigour).

## 4. Goals and non-goals

### Goals (24-hour MVP)
1. Deliver **6 lawyer-reviewed playbooks** in English, Hindi, Marathi, each usable in under 10 seconds from app open.
2. Provide **grounded Q&A** over a curated corpus of official law text with exact citations and a hard refusal path.
3. Work **offline** for all playbooks and helplines.
4. Accept **voice input** and play **spoken playbooks** (subject to the cut order).
5. Demonstrate **measurable accuracy**: a 40-question evaluation set with 100% pass on refusal and trap cases.

### Non-goals (MVP)
- Document or image scanning/OCR (post-MVP).
- Lawyer marketplace, consultations, payments.
- Drafting legal documents or notices.
- Case-law research, court-case tracking.
- State-specific laws (Maharashtra comes after MVP).
- User accounts, saved history, notifications.
- A native Android build (we ship an installable PWA).
- Giving individual legal advice or predicting case outcomes.

## 5. Product principles

1. **Grounded truth only** — if we cannot point to the law text, we do not say it.
2. **Situation first, statute second** — start from "what happened to me".
3. **One tap, no reading required** — icons, large buttons, voice.
4. **Offline-first for the critical path.**
5. **Honest labelling** — verified vs. sourced vs. refused are visibly different.
6. **Store nothing personal.**
7. **Calm tone** — short sentences, no legal jargon without explanation.

## 6. Scope — feature list

| ID | Feature | Priority | Cut order (1 = cut first) |
|----|---------|----------|---------------------------|
| F01 | Language selection (हिंदी / मराठी / English), remembered | P0 | — |
| F02 | Home screen: 112 pinned, big mic, situation icon grid | P0 | — |
| F03 | Guided triage (≤3 big-button questions) + safety routing | P0 | — |
| F04 | Verified playbooks (6) in 3 languages | P0 | extra playbooks beyond 6 → cut 2 |
| F05 | "Show this to the officer" full-screen card | P0 | — |
| F06 | Grounded Q&A (Tier 2) with citations | P0 | — |
| F07 | Grounding guard (quote verification) + refusal (Tier 3) | P0 | — |
| F08 | Voice input (Hindi, English, Marathi) | P1 | Marathi voice → cut 4 |
| F09 | Audio playback of playbooks | P1 | cut 5 |
| F10 | Offline PWA (shell, playbooks, helplines, audio) | P0 | **never cut** |
| F11 | Share-my-location action (SMS/WhatsApp link) | P2 | cut 3 |
| F12 | Freshness watcher + admin review page | P2 | cut 1 |
| F13 | LLM provider pool (eligibility, latency pick, fallback, demo pin) | P0 | — |
| F14 | Helplines directory (single sourced JSON) | P0 | — |
| F15 | Ingestion pipeline for official texts | P0 | — |
| F16 | Evaluation harness (40-question test set) | P0 | — |
| F17 | Labels, disclaimers and tier badges | P0 | — |

**The six Tier-1 playbooks:** (1) harassment on a train or public transport, (2) police refusing to register an FIR, (3) rights on arrest or detention, (4) cyber / UPI fraud, (5) domestic violence, (6) road accident.
**Bonus playbooks (only if time allows, in this order):** consumer refund or cheating; tenant–landlord eviction; workplace harassment; lost documents or theft.

## 7. Content tiers

| Tier | What the user sees | Label | Source of truth |
|---|---|---|---|
| **1 — Verified playbook** | Pre-written steps + exact law text + helplines | ✅ *Verified playbook — reviewed by a practising advocate* | Playbook JSON signed off by the advocate |
| **2 — From the law** | Verbatim section text first, then a plain-language summary built only from verified quotes | 📖 *From the law — Based on <Act §>* | Retrieved chunks from the official corpus |
| **3 — Cannot confirm** | "I can't confirm this from the law text." + helplines | ⚠️ *Not confirmed* | None — refusal |

## 8. User stories and acceptance (summary)

| ID | Story | Acceptance |
|---|---|---|
| US-1 | As a commuter being harassed, I open the app and reach "what to do now" in ≤3 taps without typing. | F01–F05 pass; time-to-first-instruction ≤10 s on demo phone |
| US-2 | As someone who cannot read well, I hear the steps in my language. | F09: audio per step, plays on tap, works offline |
| US-3 | As a user on a train with no signal, I still see the playbook and can call 139/112. | F10 airplane-mode test passes |
| US-4 | As a user, I speak "police are not taking my complaint" and get the right playbook. | F08 + F03 route to Playbook 2 in ≥90% of test phrasings |
| US-5 | As a user, I ask something outside the corpus and the app tells me it can't confirm. | F07: 100% refusal on out-of-scope set |
| US-6 | As a helper, I can show an officer the exact law text. | F05 card shows Act, section, verbatim text, source link |
| US-7 | As a reviewer, I can see which answers were verified by an advocate. | F17: badge appears only when `reviewed = true` |

## 9. Success metrics

**Hackathon metrics (what we show judges)**
- Eval pass rate: **100%** on refusals and traps; ≥90% on in-scope questions.
- Time from open to first instruction: ≤10 s (cold, demo phone).
- Offline demo works with airplane mode on.
- Zero ungrounded sentences shown across the demo path (guard logs).
- 3 languages end-to-end for text; voice per cut order.

**Product metrics (post-hackathon pilot, counters only, no personal data)**
- Playbook opens per situation; refusal rate; share of sessions using voice; offline sessions; median time-to-instruction.

## 10. Differentiation

- **Refuses rather than guesses** — enforced in code by exact-quote verification, not by a prompt promise.
- **Situation-first**, not statute-first.
- **Voice + audio + offline** for low-literacy, low-connectivity users.
- **Visible trust model:** three tiers, advocate-signed playbooks.
- **New-law aware:** BNS/BNSS/BSA primary with an old-to-new mapping for people who still say "IPC 354".

*Similar products exist (including products with similar names, see R07). Our wedge is the guarded, offline, voice-first emergency flow for ordinary citizens, not a lawyer practice-management tool.*

## 11. Business and sustainability

- **Free for citizens, always.** No ads, no selling data.
- **Funding paths:** legal-aid bodies (NALSA / state authorities), law-college legal-aid clinics, NGOs (women's safety, consumer rights), CSR grants.
- **Cost structure:** cached playbooks and audio keep running cost low; LLM usage is limited to triage and Tier-2 questions. Measure and quote *cost per 1,000 queries* from our own tests.
- **Scale path:** more states and languages are mostly content work; each addition goes through the same review pipeline.

## 12. Constraints

- 24-hour build, 3 engineers actively building (+ Dev D duties absorbed by the Lead).
- No pre-written code; content/design/data/accounts prepared in the 10-day prep window.
- Free/low-cost API tiers; models must pass our eval before entering the pool.
- No sponsor technology is mandated for Track 3.

## 13. Release plan

| Release | Contents |
|---|---|
| **MVP (hackathon)** | F01–F10, F13–F17; F11/F12 if time |
| **v1.1** | More playbooks, Maharashtra-specific content, Android Play Store package |
| **v2** | Document/image scan with consent and retention design, NGO/lawyer connect via partners, more languages |

## 14. Open questions

1. Final app name (see R07).
2. Exact scoring weights for Track 3 (unknown — assume innovation, impact, technical depth, UX, working prototype).
3. Which Tier-2 topics beyond the 6 playbooks are worth indexing in the corpus (decide at prep day 7).
