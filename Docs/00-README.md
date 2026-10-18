# LawSathi — Project Documentation Pack

| | |
|---|---|
| **Version** | 0.1 (draft for team confirmation) |
| **Date** | 2026-10-09 |
| **Event** | VIT CODE APEX 3.0 — Track 3: Open Innovation (24-hour build) |
| **Working name** | LawSathi (`APP_NAME` config value — see risk R07 in doc 12) |
| **Product in one line** | A voice-first, offline-capable app that tells ordinary people in India what to do, which law applies and whom to call — in Hindi, Marathi or English — and answers *only* from the text of the law. |

---

## 1. Reading order

| # | File | Purpose | Primary reader |
|---|------|---------|----------------|
| 01 | `01-PRD.md` | Why we are building this, for whom, what is in/out of scope | Everyone, judges' story |
| 02 | `02-SRS.md` | Testable requirements (FR/NFR) per feature | Everyone |
| 03 | `03-SDD.md` | How each part is designed (modules, algorithms, data, UI) | Engineers |
| 04 | `04-TEAM-ROLES.md` | Who owns what, working agreements, load plan | Everyone |
| 05 | `05-ARCHITECTURE-API.md` | Diagrams, API contract, content contracts, env vars | Engineers |
| 06 | `06-COMMIT-PLAN.md` | Commit-by-commit task assignment for the 24 hours | Everyone |
| 07 | `07-TEST-PLAN.md` | Tests to run for every feature, eval harness, go/no-go | Everyone |
| 08 | `08-DATA-SOURCES-LEGAL-KNOWLEDGE.md` | Official sources, ingestion, legal knowledge map, helplines | Content + data owners |
| 09 | `09-PLAYBOOK-CONTENT-SPEC.md` | Playbook format, authoring and translation rules, sign-off | Content owners, lawyer |
| 10 | `10-PREP-AND-24H-SCHEDULE.md` | 10-day prep calendar and hour-by-hour build plan with cut triggers | Everyone |
| 11 | `11-DEMO-AND-PITCH.md` | Demo script, fallback plan, judge Q&A | Presenter |
| 12 | `12-RISKS-AND-DECISIONS.md` | Risk register and decision log (ADRs) | Everyone |
| 13 | `13-PRIVACY-SECURITY-DISCLAIMERS.md` | Data inventory, consent copy, security checklist, safety routing | Everyone, judges |

## 2. Conventions used across all documents

- **Feature IDs `F01`–`F17`** are the common key. The same ID appears in the PRD, SRS, test plan and commit plan.
- **Requirement IDs** look like `F06-R3` (feature 06, requirement 3). Non-functional requirements are `NFR-xx`.
- **Test IDs** look like `F06-T2`. The commit plan lists which test IDs gate each commit.
- **Commit IDs** `C01`–`C45` are planning labels, not git hashes.
- **Decision IDs** `ADR-001`… and **risk IDs** `R01`… live in doc 12.
- **Hour markers** `H0`…`H24` are measured from the official start of the hackathon clock.
- **Priority:** P0 = must work in the demo, P1 = should, P2 = bonus (first to be cut).

## 3. Non-negotiable rules (read before anything else)

1. **Grounded only.** No sentence of legal content reaches the user unless it is (a) verbatim law text, or (b) a lawyer-reviewed playbook, or (c) a summary built only from verified quotes (see F07).
2. **Honest labels.** The ✅ *Verified playbook* badge appears only on a playbook whose `reviewed` flag was set after the advocate's sign-off. Nothing else may use it.
3. **No code before the clock starts.** Prep period = content, data, designs, accounts, documents. This pack deliberately contains no executable code: data models are tables and field lists, and API contracts are JSON examples. *Confirm in writing with the organizers that design documents with contract examples are acceptable, and that AI coding tools are allowed during the 24 hours.* (Open item O1 below.)
4. **Sources must be official and dated.** Section numbers, helpline numbers and their hours are copied from official sources, never from memory or from model output. Items in this pack marked ⚠️ *VERIFY* are research pointers only.
5. **Store nothing personal.** No login, no saved queries, no saved audio, no saved location. See doc 13 for what is still sent to third-party services and how we disclose it.
6. **Always 112 first.** Every screen offers a one-tap path to 112.

## 4. Open items that need a human answer before H0

| ID | Item | Owner | Due |
|----|------|-------|-----|
| O1 | Written confirmation from organizers: (a) prep material scope, (b) AI coding tools allowed, (c) design docs with contract examples allowed | Lead | Prep day 1 |
| O2 | Exact clock start date/time | Lead | Prep day 1 |
| O3 | Advocate review date (target prep day 5–6) and 45-minute slot | Content owner | Prep day 2 |
| O4 | Named native reader for Hindi and Marathi (everyone reads all three; name one per language as sign-off owner) | Team | Prep day 3 |
| O5 | Gemini API quota is separate from the Pro subscription — verify in the API console | Lead | Prep day 2 |
| O6 | Provider data-use terms (free tiers may use inputs to improve models) — decide which tier to use for the demo | Lead | Prep day 3 |
| O7 | Confirm the final app name and run a final search/domain/Play Store check | Team | Prep day 3 |

## 5. How to use this pack

- Treat **docs 01–03** as the contract of *what* and *how*.
- Treat **docs 06 and 10** as the daily operating plan; update status columns during the event.
- Treat **doc 07** as the definition of "done": a feature is not finished until its tests pass on the demo phone.
- Update `12-RISKS-AND-DECISIONS.md` whenever a decision changes. Do not change scope silently.
