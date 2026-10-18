# 08 — Data Sources and Legal Knowledge

**Version:** 0.1 · **Date:** 2026-10-09
**Read this first:** this document is a *research and process plan*. It tells the content owners **where to look and how to verify**. Anything marked ⚠️ **VERIFY** is a pointer from memory or secondary reading and must not be copied into the app until checked against the official text. This is general information for building the product, not legal advice.

---

## 1. Principles

1. **Official first.** Primary sources are government publications (Gazette, India Code, ministry portals). Blogs, commentaries and model memory are never sources of law text.
2. **Every item has provenance:** source URL, retrieval date, content hash, who verified it.
3. **Law text is quoted verbatim;** our own words appear only in playbooks (advocate-reviewed) and in summaries built from verified quotes.
4. **Current law:** BNS, BNSS and BSA (in force since July 2024) are primary. The old IPC/CrPC/Evidence Act appear only through the mapping table.
5. **No case law in the corpus for the MVP.** If a playbook relies on a judgment, the advocate supplies the citation and an official source link, and it appears only inside that reviewed playbook.
6. **No scanned commentary books** in the MVP (copyright, OCR error risk, not the law itself).

## 2. Source registry

URLs are the expected official homes — **confirm each on prep day 1** and record the date.

| Source | Expected URL | Use | Notes |
|---|---|---|---|
| India Code (Legislative Dept.) | indiacode.nic.in | Acts, sections, official text | Primary for central Acts; check version dates |
| Legislative Department | legislative.gov.in | Constitution, Acts | Constitution text (note: an authoritative Hindi text exists for the Constitution) |
| e-Gazette | egazette.gov.in | Notifications, commencement, amendments | Used by the watcher (P2) |
| Ministry of Home Affairs | mha.gov.in | BNS, BNSS, BSA texts; comparison/mapping tables | Look for official correspondence tables IPC↔BNS, CrPC↔BNSS, IEA↔BSA |
| Indian Railways / RailMadad | railmadad.indianrailways.gov.in | Helpline 139, complaint channels | Parliament replies also state 139 is integrated with the emergency response system |
| Emergency Response (112) | 112.gov.in | 112 details | |
| National Cyber Crime Portal | cybercrime.gov.in | 1930, online reporting | |
| NALSA | nalsa.gov.in | Legal-aid helpline and eligibility | Hours conflict between secondary sources — verify |
| National Commission for Women | ncw.nic.in | Women's helplines and complaint routes | |
| PIB | pib.gov.in | Press releases confirming helplines/schemes | Supporting evidence only |
| Ministry of Road Transport & Highways | morth.nic.in | Road accident rules/helplines | |
| RBI (customer protection) | rbi.org.in | Rules on unauthorised electronic transactions | Pointer for the cyber-fraud playbook |

## 3. Corpus plan (what we ingest)

| Priority | Act / text | Why it is needed | Ingest scope |
|---|---|---|---|
| P0 | Bharatiya Nyaya Sanhita, 2023 | Offences against women, assault, stalking, cheating, hurt, rash driving, cruelty | Relevant chapters in full (offences against body, women/children, property/cheating) |
| P0 | Bharatiya Nagarik Suraksha Sanhita, 2023 | FIR, zero FIR, arrest, rights on arrest, magistrate remedies | Chapters on information to police/FIR, arrest, production before magistrate |
| P0 | Constitution of India | Articles on equality, personal liberty, protection on arrest | Part III (fundamental rights) in full; other Articles only if cited by a playbook |
| P0 | Railways Act, 1989 | Offences and nuisance on trains/stations, railway police context | Offences/penalties chapter and passenger-safety provisions |
| P0 | Protection of Women from Domestic Violence Act, 2005 | Protection orders, protection officers, shelter | Whole Act (short) |
| P0 | Information Technology Act, 2000 | Cyber offences, identity theft/cheating by personation, privacy | Offence sections used by the cyber playbook |
| P0 | Motor Vehicles Act, 1988 (as amended) | Duties after accidents, assistance to victims, bystander protection | Accident-related chapters |
| P1 | Bharatiya Sakshya Adhiniyam, 2023 | Electronic evidence (screenshots, call records) | Electronic-evidence provisions only |
| P1 | Legal Services Authorities Act, 1987 | Eligibility for free legal aid | Eligibility sections |
| P2 | Consumer Protection Act, 2019 | Bonus playbook (refund/cheating) | Complaint and remedy chapters |
| P2 | Sexual Harassment of Women at Workplace Act, 2013 | Bonus playbook (workplace) | Whole Act |
| Later | State laws (Maharashtra first) | State police/rent rules | Post-MVP |

## 4. Legal knowledge map (research pointers per playbook)

For each playbook the content owner (1) finds the exact provisions in the official text, (2) quotes them with section IDs, (3) drafts steps from those quotes only, (4) sends to the advocate. The "candidates" below are **starting points to look up, not facts to publish**.

### P1 — Harassment on a train or public transport
- **Look up:** BNS provisions on assault or criminal force to a woman, sexual harassment, stalking, words/gestures insulting modesty (⚠️ VERIFY exact BNS section numbers and wording); Railways Act provisions on misbehaviour/nuisance on trains (⚠️ VERIFY); BNSS provisions on how and where a complaint/FIR can be filed, including filing at any police station and transfer to the right jurisdiction (⚠️ VERIFY).
- **Practical content (needs advocate + official-source check):** railway channels (139 / RailMadad), RPF/GRP, TTE/guard, emergency chain-pulling rules (⚠️ VERIFY what the Railways Act says), keeping evidence (ticket, seat number, time, witnesses, photos), what not to do.
- **Never state:** punishments or time limits unless copied from the text.

### P2 — Police refusing to register an FIR
- **Look up:** BNSS provisions on recording information of a cognizable offence, giving a copy to the informant, sending information to the superior officer when refused, and approaching the magistrate (⚠️ VERIFY exact BNSS sections); zero-FIR and e-complaint provisions (⚠️ VERIFY).
- **Practical:** written complaint with acknowledgement, registered post to the senior officer, magistrate route; advocate to confirm the correct steps and wording.

### P3 — Rights on arrest or detention
- **Look up:** Constitution Article on protection against arrest and detention and the article on personal liberty (⚠️ VERIFY article numbers); BNSS provisions on informing grounds of arrest, informing a relative/friend, medical examination, producing before a magistrate within the stated time (⚠️ VERIFY).
- **Practical:** what to ask the officer, what to say, how to reach legal aid (NALSA).
- **Note:** landmark guidelines from judgments may exist; use only if the advocate supplies the official citation and it sits inside the reviewed playbook.

### P4 — Cyber / UPI fraud
- **Look up:** IT Act offence sections on cheating by personation / identity-related offences (⚠️ VERIFY); BNS cheating provisions (⚠️ VERIFY); bank-liability rules for unauthorised transactions (RBI directions ⚠️ VERIFY current wording and time limits).
- **Practical:** call **1930** quickly, report on the national portal, contact the bank, block cards/UPI, keep screenshots and transaction IDs.
- **Never state** reversal guarantees or timelines unless copied from the official text.

### P5 — Domestic violence
- **Look up:** PWDVA provisions on protection orders, residence orders, protection officers, shelter homes and service providers (⚠️ VERIFY); BNS provisions on cruelty by husband or relatives (⚠️ VERIFY).
- **Practical:** 112, women helpline (181), protection officer, free legal aid; safety-first language, no confrontational advice.
- **Safety:** this playbook's text and audio must be reviewed for safety by the advocate and a woman reviewer if possible.

### P6 — Road accident
- **Look up:** Motor Vehicles Act provisions on duty of drivers after an accident, assistance to victims, protection for bystanders who help (⚠️ VERIFY section and wording), compensation claim process (⚠️ VERIFY); BNS provisions on rash driving/causing death by negligence — **⚠️ VERIFY which provisions are in force today, including any hit-and-run provisions whose application was discussed publicly**.
- **Practical:** 112, ambulance, move to safety, record vehicle number, informing police, insurance claim documents.

## 5. IPC/CrPC/IEA → BNS/BNSS/BSA mapping table

| Field | Notes |
|---|---|
| old_act, old_section | e.g. IPC + number |
| new_act, new_section | BNS/BNSS/BSA + number |
| note | "same", "merged", "split", "changed wording" as stated in the official table |
| source_url, verified_on | Official correspondence table (MHA/Legislative) |

Process: enter only rows needed by the playbooks and common public usage (the ~30 provisions people actually say aloud); the advocate spot-checks 10 rows.

## 6. Ingestion pipeline (what C07 implements; prep = obtaining and cleaning inputs)

| Step | Action | Quality check |
|---|---|---|
| 1 Acquire | Download official PDF/HTML; record URL, date, version | Source is on the official list |
| 2 Extract | Text extraction. If the PDF is scanned, OCR **in prep only** and proof-read | All digits and section numbers hand-checked on the sections we use |
| 3 Clean | Remove headers/footers, fix hyphenation, keep sub-section numbering and provisos | Diff against PDF on 5% random sections |
| 4 Split | One chunk per section; long sections split at sub-sections with a shared ID and `part` | Chunk count equals official table of contents |
| 5 Metadata | Act, chapter, section number, heading, language, source URL, date, hash | No empty fields |
| 6 Load | Insert; idempotent re-run | No duplicates |
| 7 Embed | Pinned embedding model; record ID and dimension | All rows embedded |
| 8 Report | Counts per Act; shortest/longest chunks; anomalies | Reviewed by Dev C and Lead |

**Corpus-ready definition:** all P0 Acts loaded; counts match; spot-check passed; hashes stored; mapping table loaded.

## 7. Language handling for law text

- Quote in the **language of the official text** (usually English; Hindi where an official Hindi text exists and is used). Never machine-translate a quote and present it as law text.
- Show a **plain-language line** in the user's language beneath each quote, clearly styled as an explanation, not as the law.
- Retrieval runs on the English law text (ADR-007). Hindi/Marathi queries are translated to English for retrieval only.
- Legal terms use the glossary (§9) so the same word is used in text and audio.

## 8. Helplines data (single source: `content/helplines.json`)

Status values: `verified` (confirmed on an official source on the recorded date), `conflicting` (sources disagree), `unverified` (seen in secondary sources only). **The UI shows only `verified` entries, or shows uncertainty for `conflicting` hours.**

| Service | Number | What we know on 2026-10-09 | Status to set |
|---|---|---|---|
| National emergency | 112 | Listed consistently as the single emergency number in several secondary sources | `unverified` → confirm on 112.gov.in |
| Railways passenger helpline | 139 | Parliament replies from the Railways ministry say complaints go through RailMadad or 139 (integrated with the emergency response system) | `unverified` → confirm on official railway portal |
| Railways security (old) | 182 | Reported as merged into 139; some sites still list it | **Do not use** unless officially confirmed |
| Women helpline | 181 | Listed in multiple secondary sources | `unverified` → confirm (NCW/MWCD) |
| Women in distress (older) | 1091 | Described as older but still active in some places | Secondary; show only if confirmed |
| Cyber crime | 1930 | Listed consistently for financial cyber fraud | `unverified` → confirm on cybercrime.gov.in |
| Legal aid (NALSA) | 15100 | Hours conflict between sources (24×7 vs weekday office hours) | `conflicting` → confirm on nalsa.gov.in, **do not claim 24×7** |
| Childline | 1098 | Appeared in a listing | `unverified` → confirm |
| Tele-MANAS (mental health) | 14416 (and a toll-free form) | Appeared in an official education-ministry listing | `unverified` → confirm |
| NCW helpline | 7827170170 | Appeared in listings | `unverified` → confirm |
| National highways emergency | 1033 | Appeared in a listing | `unverified` → confirm |

**Verification protocol:** open the official site, screenshot the number and hours, record URL + date + verifier in the JSON, and have a second person re-check. Re-verify **on the morning of the demo**.

## 9. Glossary (consistent terms across text and audio)

Native readers fill the right-hand columns; suggestions below are starting points to check.

| English term | Plain meaning (en) | Hindi (suggested) | Marathi (suggested) | Checked by |
|---|---|---|---|---|
| FIR | Police record of a crime report | एफ़आईआर (प्राथमिकी) | एफ.आय.आर. (प्रथम माहिती अहवाल) | |
| Complaint | Written or spoken report to police/authority | शिकायत | तक्रार | |
| Arrest | Police taking a person into custody | गिरफ़्तारी | अटक | |
| Magistrate | Judge who handles early criminal steps | मजिस्ट्रेट | दंडाधिकारी | |
| Bail | Release while the case continues | ज़मानत | जामीन | |
| Legal aid | Free lawyer help | निःशुल्क कानूनी सहायता | मोफत कायदेशीर मदत | |
| Helpline | Phone number for help | हेल्पलाइन | हेल्पलाइन | |
| Evidence | Things that prove what happened | सबूत | पुरावा | |

Rule: keep the English term in brackets the first time a legal term appears.

## 10. Update policy

- The watcher (P2) detects change on a small set of official URLs; **a human approves** before anything changes the corpus.
- Every playbook and helpline entry carries a `verified_on` date; entries older than 30 days show a "re-verify" flag in the admin/test report.
- A change in the law triggers: edit source text → re-ingest → affected playbooks reopened for review → badge turned off until re-signed.

## 11. Copyright and use

- Acts and the Constitution are government publications. Use the official text, cite the source, and do not reproduce publisher-added commentary, headnotes or annotations.
- If unsure about reuse of a specific document, ask the advocate and quote only short sections needed by a playbook.

## 12. What we do not include (and why)

| Item | Reason |
|---|---|
| Case-law database | Verification burden; not needed for MVP |
| Commentary/bare-act books (scanned) | Copyright, OCR risk, not the law |
| Blog posts/forums | Unverified |
| Predictions or "chances of winning" | Unsafe and unverifiable |
| Personal-case advice | Outside our role; we direct to legal aid |

## 13. Advocate review workflow and sign-off record

1. Dev C sends the English masters (one file per playbook) and the 10 trap questions to the advocate by **prep day 4**.
2. 45-minute review call on **prep day 5–6**; changes tracked in a shared document.
3. Dev C updates the JSON; the advocate re-reads changed lines.
4. For each playbook the advocate confirms in writing (message/email is enough).
5. Only then is `reviewed = true` set, with `reviewed_by`, `reviewer_role`, `reviewed_on`.

**Sign-off record (one per playbook)**

| Playbook | Version/hash | Reviewer | Date | Changes made | Approved (Y/N) | Notes |
|---|---|---|---|---|---|---|
| P1 train | | | | | | |
| P2 FIR | | | | | | |
| P3 arrest | | | | | | |
| P4 cyber fraud | | | | | | |
| P5 domestic violence | | | | | | |
| P6 road accident | | | | | | |
