# 09 — Playbook Content Specification

**Version:** 0.1 · **Date:** 2026-10-09
Defines the format, authoring rules, translation procedure, audio rules and sign-off for playbooks. Content is prepared in the 10-day window; code that renders it is written in the 24 hours.

---

## 1. What a playbook is

A **playbook** is a pre-written, advocate-reviewed, fixed-format guide for one situation. The user never receives a model-generated playbook. Models may only help *find* the right one.

## 2. Playbook data contract (one file per playbook per language)

File name: `content/playbooks/<playbook_id>.<lang>.json`. The `id`, `steps[].id` and `law[].section_id` values are **identical across languages**.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | yes | Stable ID, e.g. `train_harassment` |
| `lang` | `en`/`hi`/`mr` | yes | Language of this file |
| `version` | string | yes | Content version |
| `title` | string | yes | Short title (≤ 8 words) |
| `icon` | string | yes | Icon key shared across languages |
| `summary_line` | string | yes | One calm sentence ("You are not alone. Here is what to do.") |
| `reviewed` | boolean | yes | `true` only after advocate sign-off |
| `reviewed_by` | string/null | if reviewed | Name or role as the advocate agrees to be shown |
| `reviewer_role` | string/null | if reviewed | e.g. "Practising criminal advocate" |
| `reviewed_on` | date/null | if reviewed | Sign-off date |
| `do_now` | list of steps | yes | 3 steps max |
| `who_to_call` | list of helpline refs | yes | IDs from `helplines.json` (never raw numbers) |
| `law` | list of law cards | yes | Each: `section_id`, `act`, `section`, `heading`, `quote` (verbatim, original language), `plain_line` (user's language), `source_url`, `verified_on` |
| `avoid` | list of steps | yes | Things not to do |
| `next` | list of steps | yes | What usually happens next |
| `evidence` | list of items | optional | What to keep (ticket, screenshots, IDs) |
| `triage` | object | yes | Up to 3 questions with icon choices and routing hints |
| `phrases` | list | yes | Typical user phrasings used by the static classifier (per language) |
| `officer_card` | object | yes | Which law cards go on the card + one plain line |
| `disclaimer_key` | string | yes | Key to the standard disclaimer string |

**Step object:** `id`, `text` (≤ 12 words, verb first), `audio_key`, optional `icon`.

**Rules enforced by CI:** all required fields present; same `id`s across languages; every `law[]` has non-empty `source_url`; `who_to_call` IDs exist; `reviewed = true` requires `reviewed_by` and `reviewed_on`; string lengths within limits.

## 3. Authoring template (English master)

```
Playbook: <name>              ID: <id>
Situation in one sentence (user's words): ...
Calm line: "..."

DO NOW (max 3, ≤12 words each, verb first)
 1. ...
 2. ...
 3. ...

WHO TO CALL (from helplines.json)
 - <helpline id> — when to use it

WHAT THE LAW SAYS (verbatim; one card per provision)
 - Act: ...  Section: ...  Heading: ...
   Quote: "<exact text>"
   Plain line: <one sentence, no new facts>
   Source: <official URL>   Verified on: <date>

WHAT TO AVOID
 - ...

WHAT HAPPENS NEXT
 - ...

KEEP AS PROOF (optional)
 - ...

TRIAGE (max 3 questions with icon answers)
 - Q1 ...  [answer → routing hint]

PHRASES the user might say (5–8 per language)
```

## 4. Writing rules (low-literacy, high-stress)

1. Reading level about Class 5–6; **one idea per sentence**, ≤12 words.
2. Start with a verb: "Move to a crowded coach", "Call 139".
3. No jargon without a plain explanation; English legal term in brackets the first time.
4. **Safety first, then rights, then procedure.** Never advise confrontation or self-help punishment.
5. No promises ("you will win", "police must arrest in 24 hours") unless the exact text supports it and the advocate approves.
6. Every legal statement ties to a `law[]` card; every number (time limits, amounts) must appear in a quote.
7. Helplines are references, never typed numbers.
8. Tone: calm, respectful, non-judgemental.
9. Inclusive: avoid assuming the user's gender except where the law provision itself is gender-specific; say so plainly.

## 5. Translation procedure (Hindi, Marathi)

1. Start from the **advocate-approved English master**.
2. Draft translation (model-assisted is fine) using the glossary (doc 08 §9).
3. **Native reader** edits for natural spoken language, not formal bookish language.
4. **Back-translation check:** translate the result back to English and compare sentence by sentence with the master; any meaning difference is fixed.
5. **Read aloud** once; fix anything awkward when spoken.
6. Legal quotes stay in the official text's language; only the plain lines are translated.
7. Numbers, helpline names and section numbers stay identical across languages.
8. Second reader checks the safety copy (danger, self-harm, child abuse, sexual assault) separately.
9. Record checker names and dates in the sign-off table (doc 08 §13).

## 6. Audio script rules (for C28)

- Audio is generated **only from final, checked text**.
- One file per step per language; short sentences; neutral pace.
- Helpline numbers are read digit by digit ("one-one-two").
- Section numbers are read in the user's language convention, checked by the reader.
- No audio is generated for law-card quotes longer than ~3 sentences; instead the audio reads the plain line and "Show to officer" shows the text.
- File naming: `audio/<playbook_id>/<lang>/<step_id>.mp3`.
- Re-generate whenever the text changes (CI check: text hash stored with each audio file).

## 7. Triage content (per playbook)

- At most 3 questions; each with 2–4 icon answers.
- Example question *types* (to adapt per situation): "Are you safe right now?", "Do you know the person?", "Is it still happening?", "Is anyone else with you?".
- The answers only choose which **steps to emphasise** inside the same reviewed playbook; they do not generate new legal content.
- Questions and answers are written in all three languages and checked like any other text.

## 8. Safety content (static, never model-generated)

Fixed blocks for: **immediate danger**, **self-harm**, **child abuse**, **sexual assault**. Each has a short calm opening line, 2–3 steps, and helplines. The advocate and a native reader review the English, Hindi and Marathi versions. These run before any model (doc 03 §5.3).

## 9. Quality checklist before sign-off request

☐ Every legal statement has a law card ☐ Every quote copied from the official text (diff checked) ☐ Section IDs correct and current (BNS/BNSS/BSA) ☐ No numbers/time limits outside quotes ☐ Steps ≤12 words, verb first ☐ Helplines referenced by ID ☐ Triage ≤3 questions ☐ Phrases list present ☐ Officer card defined ☐ Disclaimer key set ☐ English reviewed by Lead and Dev C ☐ Ready to send to advocate.

## 10. Example skeleton (structure only — not legal content)

```
id: example_situation
title: <short title>
summary_line: <calm sentence>
do_now:
  - id: s1  text: <verb-first instruction>
  - id: s2  text: <verb-first instruction>
  - id: s3  text: <verb-first instruction>
who_to_call: [<helpline_id>, <helpline_id>]
law:
  - section_id: <ACT>:<SECTION>
    act: <official title and year>
    quote: "<exact official text>"
    plain_line: <explanation in user's language>
    source_url: <official URL>
    verified_on: <date>
avoid: [ ... ]
next:  [ ... ]
reviewed: false
```
