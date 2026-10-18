# 11 — Demo Script, Pitch and Judge Q&A

**Version:** 0.1 · **Date:** 2026-10-09 · **Presenter:** Lead (assumed). **Backup presenter:** Dev C.
Timings assume a 3-minute demo inside a 5–7 minute slot. Adjust once the format is known.

---

## 1. The story in one breath

> "At 11 p.m. on a train, someone is harassing you. You have one bar of signal and you can't read English. What do you do?"

LawSathi answers three things: **what to do now, which law applies, whom to call** — in your language, by voice, even offline — and it **only says what it can point to in the law**.

## 2. Three claims (the whole pitch rests on these)

1. **It answers only from the law.** Every sentence traces to an exact quote; otherwise it refuses.
2. **It works offline.** The guidance is on your phone before you need it.
3. **It speaks your language.** Hindi, Marathi, English — text and voice.

## 3. Demo script (≈3:00)

| Time | Presenter does | Audience sees | Fallback if it fails |
|---|---|---|---|
| 0:00 | Say the opening line (train scene) | — | — |
| 0:20 | Open the installed app on the phone, show the language tiles, tap **मराठी** (or Hindi) | Big tiles, spoken greeting | Skip the greeting |
| 0:35 | Tap the mic, say (in Marathi/Hindi): "Someone is troubling me on the train" | Transcript appears and is editable | Tap the **train** icon instead |
| 0:50 | Answer the 3 big-button triage questions | Calm "do now" strip at the top, then the playbook | Skip triage, open playbook directly |
| 1:05 | Show playbook: ✅ **Verified — reviewed by a practising advocate**, steps, tap a play button | Audio reads the step aloud | Speak the step yourself |
| 1:25 | Tap **Call 139**, then show **112 pinned** | Dialer opens (do not dial) | Show screenshot |
| 1:35 | Tap **Show to officer** | Full-screen card with Act, section, exact text | — |
| 1:50 | Go to **Ask**: type an in-scope question; show 📖 *From the law* with quotes first | Verbatim quote + source + "last verified" | Use cached demo answer |
| 2:10 | Ask an out-of-scope or trap question | ⚠️ "I can't confirm this from the law text" + helplines | Use cached refusal |
| 2:25 | Turn on **airplane mode**; reopen a playbook; play audio | Everything still works; "Offline" banner | Show the offline test video |
| 2:45 | (If built) show the freshness watcher flagging a seeded change for human review | Admin page with a diff | Roadmap slide |
| 2:55 | Close with the three claims and the ask | — | — |

**Demo rules:** same phone, same build, pinned model, cached answers for scripted questions, mobile data + hotspot as backup, backup video loaded on the laptop and phone, rehearsed ×3.

## 4. Slide outline (7 slides)

1. **Problem** — a person in trouble can't read the law (one real-world scenario; no invented statistics).
2. **Solution** — LawSathi in one screenshot.
3. **How it works** — situation → verified playbook → call/officer card; Ask with guard.
4. **Why you can trust it** — three tiers; exact-quote guard; advocate-signed ✅; refusal.
5. **Proof** — evaluation set results (refusal/trap 100%), offline test, latency, cost per 1,000 queries *measured by us*.
6. **Impact and sustainability** — free for citizens; partners: legal-aid bodies, clinics, NGOs, CSR; scale by content and language, not by cost.
7. **Roadmap and team** — Maharashtra/state content, more languages, document scan, Play Store; team roles.

Tech stack: one small line on slide 3 or a backup slide, not a separate section.

## 5. Judge Q&A prep

| Likely question | Answer (short) |
|---|---|
| "How do you stop hallucinations?" | The model must return an exact quote for every claim; our code checks the quote exists in the cited law text. If not, the answer is blocked and we refuse. |
| "Why not just use a general chatbot?" | A general chatbot can invent sections. We guarantee every statement is traceable, we work offline, we're voice-first in Indian languages, and we show what is verified vs. sourced. |
| "Who verified the legal content?" | A practising criminal advocate reviewed the six English playbooks; Hindi and Marathi were back-translated and read by native speakers. The ✅ badge appears only for signed-off playbooks. |
| "What if the law changes?" | A watcher flags changes on official sources for human review; nothing enters automatically; every answer shows "last verified". |
| "Isn't this legal advice?" | No. It is general legal information with sources, and it directs people to 112, helplines and free legal aid. Disclaimers are on every screen. |
| "What about privacy?" | No login, no stored queries, audio or location. Words you type or speak are sent to AI services to find the law and are not saved by us; we tell the user. |
| "Who pays and how does it scale?" | Free for citizens; funded by legal-aid bodies, college clinics, NGOs, CSR. Scale is mostly content and language review, and cached playbooks keep running cost tiny (we measured cost per 1,000 queries). |
| "How does it work without internet?" | Playbooks, helplines and audio are pre-cached by a service worker; only Ask and voice need a connection. |
| "How accurate is your voice recognition in Marathi?" | We tested ten sentences per language at hour 2; [result]. Where it falls short we fall back to icons and typing. Be honest. |
| "Do similar apps exist?" | Yes, some legal-assistant products exist (including names similar to ours). Ours is aimed at citizens in emergencies: guarded answers, offline, voice-first. (See R07.) |
| "What's innovative technically?" | Deterministic quote verification between model and user; model pool that only admits models passing our own evaluation; offline-first emergency path. |
| "What would you do with more time?" | State-specific law, more playbooks and languages, Play Store release, document scan with consent, partner integrations. |

## 6. Roles on stage

| Person | Job |
|---|---|
| Presenter | Narration and phone |
| Dev C | Second phone/laptop ready; takes over if the presenter is unavailable |
| Dev B | Timekeeper; keeps backup video ready; fields UI questions |
| Everyone | Know the cut order and the fallback for each step |

## 7. Rehearsal plan

- Rehearsal 1 (H21): script read-through, find broken steps.
- Rehearsal 2 (H22): full run with timing; test airplane-mode switch.
- Rehearsal 3 (H23): on the demo phone with the venue network and hotspot; record the final backup video.
- Pre-demo: reload the app, confirm pin and cached answers, charge devices, mute notifications, disable auto-lock, set brightness.

## 8. Honesty rules for the pitch

- Do not call any playbook "reviewed" if it is not signed.
- Do not claim 24×7 for any helpline that has conflicting hours.
- Show real measured numbers only; say "in our tests of 40 questions".
- If a feature was cut, say it is on the roadmap.
