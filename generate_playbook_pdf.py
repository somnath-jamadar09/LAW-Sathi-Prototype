import json
import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, "content")
OUTPUT_DIR = os.path.join(BASE_DIR, "playbooks_pdf")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

helplines_data = load_json(os.path.join(CONTENT_DIR, "helplines.json"))["items"]
helplines_map = {h["id"]: h for h in helplines_data}

CSS_STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

@page {
    size: A4;
    margin: 10mm 12mm;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Plus Jakarta Sans', 'Noto Sans Devanagari', 'Nirmala UI', system-ui, sans-serif;
    color: #0f172a;
    background-color: #ffffff;
    line-height: 1.45;
    font-size: 11pt;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

.page {
    page-break-after: always;
    padding: 6px 0;
}

.page:last-child {
    page-break-after: avoid;
}

.header {
    border-bottom: 2px solid #0284c7;
    padding-bottom: 8px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.app-brand {
    display: flex;
    align-items: center;
    gap: 8px;
}

.brand-badge {
    background: #0284c7;
    color: #ffffff;
    font-weight: 800;
    font-size: 11pt;
    padding: 3px 8px;
    border-radius: 6px;
    letter-spacing: 0.5px;
}

.brand-subtitle {
    font-size: 8.5pt;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.75px;
}

.playbook-badge {
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    color: #334155;
    padding: 4px 10px;
    border-radius: 999px;
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 12px;
    margin-bottom: 14px;
    position: relative;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.hero-tag {
    display: inline-block;
    background: #38bdf8;
    color: #0f172a;
    font-size: 8pt;
    font-weight: 800;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 4px;
    margin-bottom: 6px;
    letter-spacing: 0.5px;
}

.hero h1 {
    font-size: 18pt;
    font-weight: 800;
    margin-bottom: 4px;
    line-height: 1.25;
}

.hero .summary {
    font-size: 10.5pt;
    color: #cbd5e1;
    font-weight: 500;
}

.emergency-bar {
    background: #fef2f2;
    border-left: 5px solid #ef4444;
    border-top: 1px solid #fee2e2;
    border-right: 1px solid #fee2e2;
    border-bottom: 1px solid #fee2e2;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.emergency-text {
    font-size: 9.5pt;
    color: #991b1b;
    font-weight: 600;
}

.emergency-btn {
    background: #dc2626;
    color: white;
    font-weight: 800;
    font-size: 10pt;
    padding: 5px 14px;
    border-radius: 6px;
    letter-spacing: 0.5px;
    text-align: center;
}

.section-title {
    font-size: 12pt;
    font-weight: 800;
    color: #0f172a;
    margin-top: 14px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
}

.section-title .icon-bullet {
    width: 20px;
    height: 20px;
    border-radius: 5px;
    background: #0284c7;
    color: white;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 9pt;
    font-weight: bold;
}

.do-now-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 14px;
}

.step-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-top: 4px solid #0284c7;
    border-radius: 8px;
    padding: 10px;
    position: relative;
}

.step-num {
    font-size: 8pt;
    font-weight: 800;
    color: #0284c7;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.step-text {
    font-size: 10pt;
    font-weight: 700;
    color: #1e293b;
    line-height: 1.35;
}

.officer-card {
    background: #090d16;
    color: #f8fafc;
    border: 2px solid #38bdf8;
    border-radius: 10px;
    padding: 14px 16px;
    margin: 14px 0;
    page-break-inside: avoid;
}

.officer-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #334155;
    padding-bottom: 6px;
    margin-bottom: 8px;
}

.officer-badge {
    background: #38bdf8;
    color: #090d16;
    font-size: 8pt;
    font-weight: 800;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

.officer-title {
    font-size: 11pt;
    font-weight: 800;
    color: #ffffff;
}

.officer-statement {
    font-size: 10.5pt;
    font-weight: 600;
    color: #e2e8f0;
    line-height: 1.4;
    margin-bottom: 8px;
}

.officer-citations {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    color: #38bdf8;
    font-weight: 500;
}

.law-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    margin-bottom: 10px;
    padding: 10px 14px;
    page-break-inside: avoid;
}

.law-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 4px;
}

.law-section {
    font-size: 10.5pt;
    font-weight: 800;
    color: #0369a1;
}

.law-act {
    font-size: 8pt;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
}

.law-quote {
    font-size: 9pt;
    color: #334155;
    background: #f1f5f9;
    border-left: 3px solid #94a3b8;
    padding: 6px 10px;
    border-radius: 0 4px 4px 0;
    margin: 6px 0;
    font-style: italic;
    line-height: 1.4;
}

.law-plain {
    font-size: 9.5pt;
    font-weight: 600;
    color: #0f172a;
    line-height: 1.35;
}

.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 12px 0;
    page-break-inside: avoid;
}

.box-avoid {
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 4px solid #e11d48;
    border-radius: 8px;
    padding: 10px 12px;
}

.box-next {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-left: 4px solid #16a34a;
    border-radius: 8px;
    padding: 10px 12px;
}

.box-title {
    font-size: 9.5pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.box-avoid .box-title { color: #be123c; }
.box-next .box-title { color: #15803d; }

.item-list {
    list-style: none;
}

.item-list li {
    font-size: 9pt;
    font-weight: 600;
    color: #334155;
    margin-bottom: 5px;
    padding-left: 16px;
    position: relative;
    line-height: 1.35;
}

.box-avoid .item-list li::before {
    content: "✕";
    position: absolute;
    left: 0;
    color: #e11d48;
    font-weight: 800;
}

.box-next .item-list li::before {
    content: "➔";
    position: absolute;
    left: 0;
    color: #16a34a;
    font-weight: 800;
}

.evidence-box {
    background: #f8fafc;
    border: 1px dashed #94a3b8;
    border-radius: 8px;
    padding: 10px 12px;
    margin-bottom: 12px;
    page-break-inside: avoid;
}

.evidence-title {
    font-size: 9.5pt;
    font-weight: 800;
    color: #334155;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.evidence-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 14px;
}

.evidence-item {
    font-size: 8.5pt;
    color: #1e293b;
    font-weight: 500;
    display: flex;
    align-items: baseline;
    gap: 6px;
}

.evidence-item::before {
    content: "☐";
    font-size: 9.5pt;
    color: #0284c7;
    font-weight: bold;
}

.helplines-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin: 10px 0;
    page-break-inside: avoid;
}

.helpline-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 6px 8px;
    text-align: center;
}

.helpline-num {
    font-size: 13pt;
    font-weight: 800;
    color: #0284c7;
    line-height: 1.1;
}

.helpline-name {
    font-size: 7.5pt;
    font-weight: 700;
    color: #334155;
    margin-top: 2px;
    line-height: 1.2;
}

.triage-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
}

.triage-table th {
    background: #f1f5f9;
    color: #334155;
    font-weight: 700;
    text-align: left;
    padding: 6px 8px;
    border: 1px solid #cbd5e1;
}

.triage-table td {
    padding: 6px 8px;
    border: 1px solid #e2e8f0;
    vertical-align: top;
}

.signoff-box {
    margin-top: 14px;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 14px;
    background: #f8fafc;
    font-size: 8pt;
    color: #475569;
    page-break-inside: avoid;
}

.signoff-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 6px;
}

.signoff-col strong {
    color: #1e293b;
    display: block;
    margin-bottom: 2px;
}

.footer {
    margin-top: 10px;
    padding-top: 6px;
    border-top: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    color: #94a3b8;
}
"""

def generate_playbook_html(pb, lang, helplines_map):
    labels = {
        "en": {
            "category": "Criminal Incident & Citizen Rights Playbook (P2)",
            "emergency_text": "In immediate physical danger or witnessing active violence?",
            "call_btn": "CALL 112",
            "do_now": "DO NOW (Take Action Immediately)",
            "step": "STEP",
            "avoid": "WHAT TO AVOID",
            "next": "WHAT HAPPENS NEXT (Escalation Path)",
            "officer_badge": "OFFICER REFERENCE CARD",
            "law_title": "WHAT THE LAW SAYS (Statutory Bare Act Provisions)",
            "evidence_title": "EVIDENCE & RECORDS TO PRESERVE",
            "triage_title": "SITUATION TRIAGE GUIDE",
            "helplines_title": "OFFICIAL CRISIS & LEGAL HELPLINES",
            "signoff_title": "ADVOCATE REVIEW & AUDIT LOG (Doc 08 §13)",
            "disclaimer": "DISCLAIMER: LawSathi provides general legal information grounded strictly in official statute text. It does not constitute individualized legal counsel or court representation. In an emergency, dial 112."
        },
        "hi": {
            "category": "अपराधिक घटना एवं नागरिक अधिकार प्लेबुक (P2)",
            "emergency_text": "क्या आप तात्कालिक शारीरिक खतरे में हैं या हिंसा के साक्षी हैं?",
            "call_btn": "112 पर कॉल करें",
            "do_now": "तुरंत क्या करें (तत्काल कदम)",
            "step": "कदम",
            "avoid": "क्या न करें (सावधानियां)",
            "next": "आगे क्या होगा (अगली कानूनी कार्रवाई)",
            "officer_badge": "पुलिस अधिकारी संदर्भ कार्ड",
            "law_title": "कानून क्या कहता है (आधिकारिक कानूनी प्रावधान)",
            "evidence_title": "संभाल कर रखने योग्य सबूत व दस्तावेज",
            "triage_title": "स्थिति वर्गीकरण मार्गदर्शन",
            "helplines_title": "आधिकारिक आपातकालीन एवं कानूनी हेल्पलाइन",
            "signoff_title": "अधिवक्ता समीक्षा एवं ऑडिट रिकॉर्ड (Doc 08 §13)",
            "disclaimer": "अस्वीकरण: LawSathi केवल आधिकारिक कानूनी पाठ पर आधारित सामान्य कानूनी जानकारी प्रदान करता है। यह व्यक्तिगत कानूनी सलाह या न्यायालयीन प्रतिनिधित्व नहीं है। आपातकाल में 112 मिलाएं।"
        },
        "mr": {
            "category": "गुन्हेगारी घटना आणि नागरिक हक्क प्लेबुक (P2)",
            "emergency_text": "तुम्ही तात्काळ शारीरिक धोक्यात आहात किंवा हिंसाचाराचे साक्षीदार आहात?",
            "call_btn": "112 वर कॉल करा",
            "do_now": "तात्काळ काय करावे (त्वरित कृती करा)",
            "step": "पायरी",
            "avoid": "काय टाळावे (सावधगिरी बाळगा)",
            "next": "पुढे काय घडेल (कायदेशीर पाठपुरावा)",
            "officer_badge": "पोलीस अधिकारी संदर्भ कार्ड",
            "law_title": "कायदा काय सांगतो (अधिकृत कायदेशीर तरतुदी)",
            "evidence_title": "जतन करावयाचे पुरावे व कागदपत्रे",
            "triage_title": "परिस्थितीनुसार मार्गदर्शन",
            "helplines_title": "अधिकृत आणीबाणी व कायदेशीर हेल्पलाइन",
            "signoff_title": "वकील पडताळणी नोंद व ऑडिट लॉग (Doc 08 §13)",
            "disclaimer": "अस्वीकरण: LawSathi केवळ अधिकृत कायद्याच्या मजकुरावर आधारित सामान्य कायदेशीर माहिती पुरवते. हा वैयक्तिक कायदेशीर सल्ला किंवा न्यायालयात प्रतिनिधित्व नाही. आणीबाणीच्या वेळी 112 डायल करा."
        }
    }
    L = labels[lang]

    # Render Do Now
    do_now_html = ""
    for idx, s in enumerate(pb["do_now"], 1):
        do_now_html += f"""
        <div class="step-card">
            <div class="step-num">{L['step']} 0{idx}</div>
            <div class="step-text">{s['text']}</div>
        </div>
        """

    # Render Law Cards
    law_cards_html = ""
    for l in pb["law"]:
        law_cards_html += f"""
        <div class="law-card">
            <div class="law-header">
                <span class="law-section">{l['section_id']} — {l['heading']}</span>
                <span class="law-act">{l['act']}</span>
            </div>
            <div class="law-quote">"{l['quote']}"</div>
            <div class="law-plain"><strong>{lang.upper()}:</strong> {l['plain_line']}</div>
        </div>
        """

    # Render Avoid & Next
    avoid_html = "".join([f"<li>{a['text']}</li>" for a in pb["avoid"]])
    next_html = "".join([f"<li>{n['text']}</li>" for n in pb["next"]])

    # Render Evidence
    evidence_html = "".join([f"<div class='evidence-item'>{e}</div>" for e in pb["evidence"]])

    # Render Helplines
    helplines_html = ""
    for hid in ["112", "15100", "1930", "181"]:
        if hid in helplines_map:
            h = helplines_map[hid]
            name = h["name"].get(lang, h["name"]["en"])
            helplines_html += f"""
            <div class="helpline-card">
                <div class="helpline-num">{h['number']}</div>
                <div class="helpline-name">{name}</div>
            </div>
            """

    # Render Triage
    triage_rows = ""
    for q in pb["triage"]["questions"]:
        opts_desc = " | ".join([f"<strong>{opt['label']}</strong>" for opt in q["options"]])
        triage_rows += f"""
        <tr>
            <td style="width: 45%; font-weight: 600;">{q['prompt']}</td>
            <td>{opts_desc}</td>
        </tr>
        """

    officer_card = pb.get("officer_card", {})

    html = f"""
    <div class="page">
        <div class="header">
            <div class="app-brand">
                <span class="brand-badge">LAWSATHI</span>
                <div>
                    <div style="font-weight: 800; font-size: 10pt; color: #0f172a;">CITIZEN EMERGENCY LEGAL COMPANION</div>
                    <div class="brand-subtitle">{L['category']} · {lang.upper()}</div>
                </div>
            </div>
            <div class="playbook-badge">
                ID: {pb['id']} · VER: {pb['version']}
            </div>
        </div>

        <div class="hero">
            <div class="hero-tag">BNSS 2023 & BNS 2023 · STATUTORY GUIDE</div>
            <h1>{pb['title']}</h1>
            <div class="summary">{pb['summary_line']}</div>
        </div>

        <div class="emergency-bar">
            <div class="emergency-text">
                🚨 <strong>{L['emergency_text']}</strong>
            </div>
            <div class="emergency-btn">{L['call_btn']}</div>
        </div>

        <div class="section-title">
            <span class="icon-bullet">1</span>
            {L['do_now']}
        </div>
        <div class="do-now-grid">
            {do_now_html}
        </div>

        <div class="officer-card">
            <div class="officer-card-header">
                <span class="officer-title">📱 {officer_card.get('title', 'SHOW TO OFFICER')}</span>
                <span class="officer-badge">{L['officer_badge']}</span>
            </div>
            <div class="officer-statement">
                "{officer_card.get('plain_line', '')}"
            </div>
            <div class="officer-citations">
                MANDATORY STATUTORY CITATION: {' · '.join(officer_card.get('law_ids', []))}
            </div>
        </div>

        <div class="two-col">
            <div class="box-avoid">
                <div class="box-title">⚠️ {L['avoid']}</div>
                <ul class="item-list">
                    {avoid_html}
                </ul>
            </div>
            <div class="box-next">
                <div class="box-title">📋 {L['next']}</div>
                <ul class="item-list">
                    {next_html}
                </ul>
            </div>
        </div>

        <div class="evidence-box">
            <div class="evidence-title">📁 {L['evidence_title']}</div>
            <div class="evidence-grid">
                {evidence_html}
            </div>
        </div>

        <div class="section-title">
            <span class="icon-bullet">2</span>
            {L['law_title']}
        </div>
        {law_cards_html}

        <div class="section-title">
            <span class="icon-bullet">3</span>
            {L['triage_title']}
        </div>
        <table class="triage-table">
            <thead>
                <tr>
                    <th>Scenario Question</th>
                    <th>Guided Routing Action</th>
                </tr>
            </thead>
            <tbody>
                {triage_rows}
            </tbody>
        </table>

        <div class="section-title" style="margin-top: 10px;">
            <span class="icon-bullet">4</span>
            {L['helplines_title']}
        </div>
        <div class="helplines-grid">
            {helplines_html}
        </div>

        <div class="signoff-box">
            <strong>{L['signoff_title']}</strong>
            <div class="signoff-grid">
                <div class="signoff-col">
                    <strong>Review Status:</strong>
                    {"✅ Verified by Advocate" if pb.get("reviewed") else "⚠️ Draft (Pending Prep Day 5–6 Advocate Sign-Off)"}
                </div>
                <div class="signoff-col">
                    <strong>Reviewing Advocate:</strong>
                    {pb.get("reviewed_by") or "Scheduled Advocate Session"}
                </div>
                <div class="signoff-col">
                    <strong>Statutory Verifier:</strong>
                    India Code / MHA Gazette 2024
                </div>
            </div>
            <div style="margin-top: 6px; font-size: 7.5pt; color: #64748b;">
                {L['disclaimer']}
            </div>
        </div>

        <div class="footer">
            <span>LawSathi · VIT CODE APEX 3.0 (Track 3: Open Innovation)</span>
            <span>Grounded Corpus · Section 173 BNSS 2023</span>
            <span>Page 1 / 1</span>
        </div>
    </div>
    """
    return html

def build_pdf(html_body, output_pdf_path):
    full_html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>{CSS_STYLES}</style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    temp_html_path = output_pdf_path.replace(".pdf", ".html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    file_url = "file:///" + os.path.abspath(temp_html_path).replace("\\", "/")
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={os.path.abspath(output_pdf_path)}",
        file_url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error building {output_pdf_path}: {res.stderr}")
    else:
        print(f"Successfully created: {output_pdf_path} ({os.path.getsize(output_pdf_path)} bytes)")
    
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

def main():
    en_pb = load_json(os.path.join(CONTENT_DIR, "playbooks", "fir_refusal.en.json"))
    hi_pb = load_json(os.path.join(CONTENT_DIR, "playbooks", "fir_refusal.hi.json"))
    mr_pb = load_json(os.path.join(CONTENT_DIR, "playbooks", "fir_refusal.mr.json"))

    # 1. English PDF
    en_html = generate_playbook_html(en_pb, "en", helplines_map)
    build_pdf(en_html, os.path.join(OUTPUT_DIR, "LawSathi_Playbook_FIR_Refusal_EN.pdf"))

    # 2. Hindi PDF
    hi_html = generate_playbook_html(hi_pb, "hi", helplines_map)
    build_pdf(hi_html, os.path.join(OUTPUT_DIR, "LawSathi_Playbook_FIR_Refusal_HI.pdf"))

    # 3. Marathi PDF
    mr_html = generate_playbook_html(mr_pb, "mr", helplines_map)
    build_pdf(mr_html, os.path.join(OUTPUT_DIR, "LawSathi_Playbook_FIR_Refusal_MR.pdf"))

    # 4. Trilingual Complete Compendium
    trilingual_html = en_html + hi_html + mr_html
    build_pdf(trilingual_html, os.path.join(OUTPUT_DIR, "LawSathi_Playbook_FIR_Refusal_Trilingual.pdf"))

if __name__ == "__main__":
    main()
