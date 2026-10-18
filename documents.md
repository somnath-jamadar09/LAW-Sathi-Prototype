# Legal Documents for Ingestion (Corpus Registry)

This document specifies the exact official legal texts, acts, and regulatory frameworks fed into the LawSathi RAG/knowledge ingestion pipeline for the actual project.

---

## 1. Primary Criminal & Procedural Codes (Current Laws - In Force 2024)

These form the backbone of the legal corpus for criminal offences, police procedures, citizen rights, and evidence handling:

1. **Bharatiya Nyaya Sanhita, 2023 (BNS)**
   - *Key Focus*: Offences against women and children, bodily harm/assault, criminal intimidation, stalking, cheating/fraud, rash driving, and domestic cruelty.
   - *Scope*: Relevant chapters in full (offences against human body, women/children, property, reputation).

2. **Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)**
   - *Key Focus*: Procedure for registering an FIR (including Section 173 for mandatory FIR & Zero FIR), e-FIR guidelines, rights on arrest & detention, mandatory medical examination, communication rights, and production before a magistrate within 24 hours.
   - *Scope*: Chapters on information to police, arrest procedures, and magistrate remedies.

3. **Bharatiya Sakshya Adhiniyam, 2023 (BSA)**
   - *Key Focus*: Admissibility and certification of electronic records and digital evidence (Section 61–63: screenshots, WhatsApp/SMS records, call logs, CCTV footage).
   - *Scope*: Electronic evidence provisions and certificate mandates.

4. **Official Legislative Concordance / Correspondence Mapping Tables (MHA / Legislative Dept.)**
   - *Key Focus*: Bi-directional cross-reference mapping:
     - IPC ↔ BNS
     - CrPC ↔ BNSS
     - Indian Evidence Act (IEA) ↔ BSA
   - *Scope*: Standard mapping for popular provisions used by citizens and legal aid workers.

---

## 2. Constitutional Framework

5. **Constitution of India (Part III: Fundamental Rights)**
   - *Key Focus*:
     - **Article 14**: Right to Equality.
     - **Article 20**: Protection in respect of conviction for offences.
     - **Article 21**: Protection of life and personal liberty.
     - **Article 22**: Protection against arrest and detention (grounds of arrest, legal representation).
   - *Scope*: Part III in full, plus constitutional remedies under Article 32 / 226.

---

## 3. Special & Domain-Specific Statutory Acts

6. **The Protection of Women from Domestic Violence Act, 2005 (PWDVA)**
   - *Key Focus*: Definitions of domestic violence, Protection Orders, Residence Orders, Monetary Relief, duties of Protection Officers, and Service Providers.
   - *Scope*: Full Act.

7. **The Information Technology Act, 2000 (IT Act, as amended)**
   - *Key Focus*: Section 43 (penalty for unauthorized access), Section 66 (computer related offences), Section 66C (identity theft), Section 66D (cheating by personation using computer resource), Section 67 (privacy / obscenity).
   - *Scope*: Chapters on cyber offences and citizen grievance remedies.

8. **The Railways Act, 1989**
   - *Key Focus*: Passenger safety, offences on trains and railway premises (Section 141 – unauthorized alarm chain pulling, Section 145 – drunkenness or nuisance, Section 146 – obstructing railway servants, Section 162 – entering carriage reserved for females).
   - *Scope*: Offences, penalties, and passenger safety chapters.

9. **The Motor Vehicles Act, 1988 (as amended by MV Amendment Act, 2019)**
   - *Key Focus*: Section 134 (duty of driver in case of accident), Section 134A (Protection of Good Samaritans / bystander protection), motor accident compensation rules.
   - *Scope*: Accident, emergency assistance, and liability chapters.

10. **The Legal Services Authorities Act, 1987**
    - *Key Focus*: Section 12 (eligibility criteria for free legal aid through NALSA, SLSA, and DLSA).
    - *Scope*: Eligibility and access provisions.

11. **The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)** *(P2 / Expansion)*
    - *Key Focus*: Internal Committee (IC) constitution, filing complaints, inquiry procedure, and interim relief.
    - *Scope*: Full Act.

12. **The Consumer Protection Act, 2019** *(P2 / Expansion)*
    - *Key Focus*: Consumer rights, e-commerce transactions, unfair trade practices, and District Commission filing mechanisms.
    - *Scope*: Complaint and remedy chapters.

---

## 4. Regulatory Directives & Statutory Citizen Guidelines

13. **Reserve Bank of India (RBI) Directives on Unauthorised Electronic Banking Transactions**
    - *Circular*: RBI/2017-18/15 DBR.No.Leg.BC.78/09.07.005/2017-18 (*Limiting Liability of Customers in Unauthorised Electronic Banking Transactions*).
    - *Key Focus*: Zero liability criteria, reporting within 3 days, maximum liability tiers for third-party breaches.

14. **Standard Operating Procedures (SOP) & Statutory Citizen Guides**
    - **Ministry of Home Affairs (MHA) - National Cyber Crime Reporting Portal (I4C)**: SOP for citizen reporting via National Helpline **1930** and `cybercrime.gov.in`.
    - **Ministry of Railways**: RailMadad citizen procedure & SOP for Helpline **139**.
    - **Emergency Response Support System (ERSS)**: Citizen SOP for Pan-India Emergency Helpline **112**.

---

## 5. Official Source Repositories (Data Provenance)

All fed texts are sourced exclusively from authentic government portals:

| Source Name | Portal URL | Target Ingestion Content |
|---|---|---|
| **India Code** | `indiacode.nic.in` | Central Acts, Sections, official amendments |
| **Legislative Department** | `legislative.gov.in` | Official Constitution of India & Gazette Acts |
| **Ministry of Home Affairs (MHA)** | `mha.gov.in` | BNS, BNSS, BSA authoritative texts & mapping tables |
| **The Gazette of India (e-Gazette)** | `egazette.gov.in` | Commencement notifications & amendment notices |
| **Reserve Bank of India (RBI)** | `rbi.org.in` | Circulars & master directions on consumer financial liability |
| **National Legal Services Authority** | `nalsa.gov.in` | Legal aid regulations & entitlement rules |

---

## 6. Corpus Ingestion Exclusions

To prevent hallucinations, copyright infringements, and legal inaccuracies:
- **No unverified commentaries or bare-act guidebooks** (avoids OCR noise and publisher annotations).
- **No generic case-law database dumps** (MVP corpus prioritizes codified statutory law and verified landmark citations).
- **No secondary blogs, forums, or third-party interpretations**.
