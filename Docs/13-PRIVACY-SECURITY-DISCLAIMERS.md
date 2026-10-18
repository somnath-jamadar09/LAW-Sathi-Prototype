# 13 — Privacy, Security, Safety Routing and Disclaimers

**Version:** 0.1 · **Date:** 2026-10-09
This is a design document, not legal advice. Have the advocate read §2 and §5 before launch. India's Digital Personal Data Protection Act, 2023 may apply to data we handle; the team should read the current Act and rules ⚠️ **VERIFY** and confirm what applies to a no-login app.

---

## 1. Promise to users (plain language)

> "We don't ask who you are. We don't save what you say, type or record, and we don't save where you are. To find the right law, your words are sent to AI services that process them for that purpose."

Be exact: **"we store nothing" is not the same as "nothing leaves your phone."** Say both parts.

## 2. Data inventory

| Data | Where it goes | Stored by us? | Retention | Disclosure |
|---|---|---|---|---|
| Language choice | Device (localStorage) | No (device only) | Until user clears | Not needed |
| Typed question text | API → LLM provider (and translation step) | **No** | Not stored by us; provider's own terms apply | Notice on Ask screen |
| Voice recording | Browser → API → speech provider | **No** | Discarded after transcription by us; provider's terms apply | **One-time consent notice before first mic use** |
| Transcript | Device; then as typed text | No | — | — |
| Conversation history | Device memory; sent with each request | No | Until the page closes | — |
| Location (F11) | Device → map link → user's chosen SMS/WhatsApp contact | **No** (never sent to our servers) | — | Permission prompt + explanation |
| IP address | API logs / rate limiter | Transient | Short-lived counters only | Mention in about page |
| Request logs | Our logs | Yes — **IDs, route, tier, latency, counts only** | Short (days) | About page |
| Eval questions | Repo / DB (our own test data) | Yes | Project lifetime | No real people's data |
| Admin actions | DB | Yes | Project lifetime | Internal |

**Rules**
- No cookies, trackers, ad SDKs or analytics that identify users. Anonymous counters (which playbook opened) only if needed.
- Logs must not contain `question`, `transcript`, `audio`, `location`, names or phone numbers. Add a test (NFR-09).
- Tell users not to type names, phone numbers or addresses into Ask ("No need to enter names or numbers.").
- Third-party processors: LLM, embedding and speech providers. Check each provider's data-use terms (O6). Free tiers may allow use of inputs to improve models — decide whether to use a paid/no-training tier for anything beyond the demo.

## 3. Consent and notice copy (English master; translate and check)

**Voice (first use):**
"To understand your voice, we send the recording to a speech service. We do not save it. Continue?" — [Yes] [Type instead]

**Ask screen (always visible, small):**
"Your question is sent to AI services to find the right law. We don't save it. Please don't enter names or phone numbers."

**Location (before the OS prompt):**
"We'll ask your phone for your location once, only to put a map link in the message you send. We don't see or save it."

**About page:** short "How we verify", "What we store", "What we don't", "Sources", "Contact".

## 4. Security checklist

| Area | Control | Test |
|---|---|---|
| Secrets | Only in host secret stores; `.env.example` names only; repo scan before each release | NFR-10 |
| Transport | HTTPS only; HSTS where supported | Check on production URL |
| CORS | Allow-list of the web origin(s) | Request from another origin blocked |
| Rate limiting | Per-IP per-minute limit; `Retry-After` | Burst test |
| Input limits | Question ≤500 chars; audio ≤30 s / ≤2 MB | Oversized request rejected |
| Prompt injection | User text is data; instructions only in system prompt; guard enforces regardless of model behaviour | F07-T7 |
| Output safety | Guard + number/section post-check; Tier-3 refusal | F07 tests |
| Admin | Secret header; unlinked route; rate-limited; no destructive actions | F12-T3 |
| Dependencies | Pin versions; no unreviewed packages added after freeze | CI |
| Supply chain | Only widely-used libraries; no copying of unknown code | Review |
| Backups | Content in git; DB can be rebuilt from ingestion | Rebuild drill (optional) |
| Error messages | Generic to users; details in logs without user text | Review |

## 5. Safety routing (before any model)

| Input signals | Fixed response (reviewed text) |
|---|---|
| Immediate physical danger ("he is hitting me", "I'm being followed") | Calm line, 3 steps (move to a safe public place, call 112, tell someone near you), 112 button |
| Self-harm or suicide cues | Kind, short message; encourage contacting a trusted person; 112 and the national mental-health helpline (verify number and hours in `helplines.json`) |
| Child in danger or abuse | 112 and the child helpline (verify); do not ask for details |
| Sexual assault | 112 and women helplines; steps on safety, medical care and preserving evidence — wording reviewed by the advocate and a woman reviewer if possible |

**Rules:** no model-generated text; same content offline (it is static); phrases in all three languages including spelling variants; false positives are acceptable (a safe screen costs little), false negatives are not — test with the phrase set (F03-T1).

## 6. Disclaimers (all three languages, every screen)

**Footer (short):** "General legal information, not legal advice. In danger? Call 112."

**About page (long):**
"LawSathi explains what the law says in simple language and points to official helplines. It is not a lawyer and does not give advice for your specific case. Verified playbooks were reviewed by a practising advocate on the date shown. Other answers come directly from the text of the law and show the source. If we cannot confirm something from the law, we say so. For your own case, speak to a lawyer or free legal aid (NALSA)."

**Do not:** claim a lawyer-client relationship; promise outcomes; suggest self-help punishment; use ✅ for anything unsigned.

## 7. Abuse and misuse considerations

| Concern | Design response |
|---|---|
| Users filing false complaints with app help | Playbooks describe lawful steps only; no templates that encourage false reports; neutral language |
| Stalkers/abusers using the app to check what a victim sees | No history on device beyond language; "quick exit" (optional P2) button to close to a neutral screen |
| Over-trust in AI | Tier badges; refusal; "not legal advice"; always point to 112/legal aid |
| Shared phones | No saved history; language preference only |
| Minors using the app | Simple language; child-safety routing; no data collection |

## 8. Accessibility as safety

Large text, voice, icons and offline are safety features: they let a frightened or low-literacy user reach help quickly. Treat NFR-05 failures as Sev-2.

## 9. Pre-launch review

☐ Advocate reads disclaimers, safety copy and consent text ☐ Native readers confirm hi/mr wording ☐ Log inspection finds no user text ☐ Provider terms recorded (O6) ☐ Keys rotated if ever exposed ☐ About page live ☐ Safety phrases tested in all languages ☐ DPDP applicability noted by the team ⚠️ VERIFY.
