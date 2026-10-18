// ─────────────────────────────────────────────────────────────────────────────
// LawSathi Prototype — Client Application Logic
// ─────────────────────────────────────────────────────────────────────────────

const API_BASE = "http://localhost:8000";

// Resolve content path relative to this script's origin (works from http.server)
// Frontend is served from prototype/frontend/, content is at ../../content/
const CONTENT_BASE = "../../content";

let currentLang = "en";
let currentPlaybook = null;
let currentPlaybookId = null; // Track ID separately so we can reload on lang switch

// ──────────── TRANSLATIONS ────────────
const TRANSLATIONS = {
  en: {
    placeholder:       "e.g. Police refusing to file my FIR…",
    askBtn:            "Ask",
    tapToSpeak:        "Tap to Speak",
    listening:         "Listening…",
    voiceUnavailable:  "Voice unavailable",
    emergencySituations: "Emergency Situations",
    doNow:             "⚡ What to Do Right Now",
    avoid:             "🚫 What to Avoid",
    emergencyNumbers:  "📞 Emergency Numbers",
    lawSays:           "📖 What the Law Says",
    ifStillRefuse:     "🔜 If They Still Refuse",
    listenBtn:         "🔊 Listen to Instructions",
    showOfficer:       "👮 Show This to the Police Officer",
    backToSituations:  "← Back to Situations",
    back:              "← Back",
    close:             "✕ Close Officer Card",
    yourQuestion:      "Your Question:",
    lawsathiGuidance:  "LawSathi Plain Guidance:",
    analysingText:     "Analyzing against official statute corpus…",
    offlineMsg:        "⚡ Offline Mode — Cached Content Active",
    immediateDanger:   "Immediate Danger?",
    tagline:           "Your legal rights. Instantly. In your language.",
    footer:            "⚖️ Answers derived strictly from the official text of the law. Not a substitute for a legal advocate.",
    comingSoon:        "playbook is queued for advocate review.",
    loadingPlaybook:   "Loading…",
    errorPlaybook:     "Unable to load playbook. Please check your connection.",
  },
  hi: {
    placeholder:       "जैसे: पुलिस मेरी एफ़आईआर दर्ज नहीं कर रही…",
    askBtn:            "पूछें",
    tapToSpeak:        "बोलने के लिए टैप करें",
    listening:         "सुन रहे हैं…",
    voiceUnavailable:  "वॉइस उपलब्ध नहीं",
    emergencySituations: "आपातकालीन स्थितियाँ",
    doNow:             "⚡ अभी क्या करें",
    avoid:             "🚫 क्या न करें",
    emergencyNumbers:  "📞 आपातकालीन नंबर",
    lawSays:           "📖 कानून क्या कहता है",
    ifStillRefuse:     "🔜 अगर वे फिर भी मना करें",
    listenBtn:         "🔊 निर्देश सुनें",
    showOfficer:       "👮 यह पुलिस अधिकारी को दिखाएं",
    backToSituations:  "← स्थितियों पर वापस जाएं",
    back:              "← वापस",
    close:             "✕ बंद करें",
    yourQuestion:      "आपका प्रश्न:",
    lawsathiGuidance:  "LawSathi का सरल मार्गदर्शन:",
    analysingText:     "आधिकारिक कानूनी धाराओं के विरुद्ध विश्लेषण हो रहा है…",
    offlineMsg:        "⚡ ऑफलाइन मोड — कैश सामग्री सक्रिय है",
    immediateDanger:   "तत्काल खतरा?",
    tagline:           "आपके कानूनी अधिकार। तुरंत। आपकी भाषा में।",
    footer:            "⚖️ उत्तर केवल कानून के आधिकारिक पाठ से दिए जाते हैं। यह किसी वकील का विकल्प नहीं है।",
    comingSoon:        "प्लेबुक समीक्षाधीन है।",
    loadingPlaybook:   "लोड हो रहा है…",
    errorPlaybook:     "प्लेबुक लोड करने में असमर्थ। कृपया अपना कनेक्शन जांचें।",
  },
  mr: {
    placeholder:       "उदा. पोलीस माझी FIR नोंदवत नाही…",
    askBtn:            "विचारा",
    tapToSpeak:        "बोलण्यासाठी टॅप करा",
    listening:         "ऐकत आहे…",
    voiceUnavailable:  "व्हॉइस उपलब्ध नाही",
    emergencySituations: "आणीबाणीच्या परिस्थिती",
    doNow:             "⚡ आत्ता काय करावे",
    avoid:             "🚫 काय टाळावे",
    emergencyNumbers:  "📞 आणीबाणी क्रमांक",
    lawSays:           "📖 कायदा काय सांगतो",
    ifStillRefuse:     "🔜 जर ते तरीही नकार देत असतील",
    listenBtn:         "🔊 सूचना ऐका",
    showOfficer:       "👮 हे पोलीस अधिकाऱ्याला दाखवा",
    backToSituations:  "← परिस्थितींवर परत जा",
    back:              "← मागे",
    close:             "✕ बंद करा",
    yourQuestion:      "तुमचा प्रश्न:",
    lawsathiGuidance:  "LawSathi चे साधे मार्गदर्शन:",
    analysingText:     "अधिकृत कायदेशीर खंडांशी विश्लेषण होत आहे…",
    offlineMsg:        "⚡ ऑफलाइन मोड — कॅश सामग्री सक्रिय आहे",
    immediateDanger:   "तात्काळ धोका?",
    tagline:           "तुमचे कायदेशीर हक्क. लगेच. तुमच्या भाषेत.",
    footer:            "⚖️ उत्तरे केवळ कायद्याच्या अधिकृत मजकुरातून दिली जातात. हे वकिलाचा पर्याय नाही.",
    comingSoon:        "प्लेबुक तपासणीसाठी रांगेत आहे.",
    loadingPlaybook:   "लोड होत आहे…",
    errorPlaybook:     "प्लेबुक लोड करण्यात अयशस्वी. कृपया आपले कनेक्शन तपासा.",
  }
};

function t(key) {
  return (TRANSLATIONS[currentLang] || TRANSLATIONS.en)[key] || TRANSLATIONS.en[key] || key;
}

// ──────────── UPDATE ALL UI TEXT ON LANG CHANGE ────────────
function applyLanguageToUI() {
  // Home view
  const input = document.getElementById("queryInput");
  if (input) input.placeholder = t("placeholder");
  const askBtn = document.getElementById("askBtn");
  if (askBtn) askBtn.textContent = t("askBtn");
  const micLabel = document.getElementById("micLabel");
  if (micLabel && !micLabel.dataset.listening) micLabel.textContent = t("tapToSpeak");
  const sectionTitle = document.querySelector(".section-title");
  if (sectionTitle) sectionTitle.textContent = t("emergencySituations");
  const tagline = document.querySelector(".brand-tagline");
  if (tagline) tagline.textContent = t("tagline");
  const danger = document.querySelector(".emergency-text strong");
  if (danger) danger.textContent = t("immediateDanger");

  // Playbook view section headers
  const doNowHeader = document.querySelector("#viewPlaybook .playbook-section:nth-of-type(1) .playbook-section-title");
  if (doNowHeader) doNowHeader.textContent = t("doNow");
  const avoidHeader = document.querySelector("#avoidSection .playbook-section-title");
  if (avoidHeader) avoidHeader.textContent = t("avoid");
  const whoHeader = document.querySelector("#viewPlaybook .playbook-section:nth-of-type(3) .playbook-section-title");
  if (whoHeader) whoHeader.textContent = t("emergencyNumbers");
  const lawHeader = document.querySelector("#viewPlaybook .playbook-section:nth-of-type(4) .playbook-section-title");
  if (lawHeader) lawHeader.textContent = t("lawSays");
  const nextHeader = document.querySelector("#nextSection .playbook-section-title");
  if (nextHeader) nextHeader.textContent = t("ifStillRefuse");
  const listenBtn = document.getElementById("playAllAudioBtn");
  if (listenBtn) listenBtn.textContent = t("listenBtn");
  const showOfficerBtn = document.getElementById("showOfficerBtn");
  if (showOfficerBtn) showOfficerBtn.textContent = t("showOfficer");
  const playbookBackBtn = document.getElementById("playbookBackBtn");
  if (playbookBackBtn) playbookBackBtn.textContent = t("backToSituations");

  // Ask result view
  const askBackBtn = document.getElementById("askBackBtn");
  if (askBackBtn) askBackBtn.textContent = t("back");
  const yourQ = document.querySelector(".user-q-display strong");
  if (yourQ) yourQ.textContent = t("yourQuestion");
  const guidance = document.querySelector(".qa-summary-box strong");
  if (guidance) guidance.textContent = t("lawsathiGuidance");

  // Officer card
  const closeBtn = document.getElementById("closeOfficerBtn");
  if (closeBtn) closeBtn.textContent = t("close");

  // Footer
  const footer = document.querySelector(".app-footer p");
  if (footer) footer.textContent = t("footer");

  // Offline banner
  const offlineEl = document.getElementById("offlineIndicator");
  if (offlineEl) offlineEl.textContent = t("offlineMsg");
}

// ──────────── VIEW CONTROLLER ────────────
const views = {
  home:       document.getElementById("viewHome"),
  playbook:   document.getElementById("viewPlaybook"),
  officer:    document.getElementById("viewOfficer"),
  askResult:  document.getElementById("viewAskResult")
};

function switchView(viewName) {
  Object.values(views).forEach(v => {
    v.classList.remove("active");
    if (v.classList.contains("officer-card-mode")) {
      v.style.display = "none";
    }
  });
  const target = views[viewName];
  if (target.classList.contains("officer-card-mode")) {
    target.style.display = "block";
    requestAnimationFrame(() => target.classList.add("active"));
  } else {
    target.classList.add("active");
  }
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// ──────────── LANGUAGE HANDLING ────────────
document.querySelectorAll(".lang-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".lang-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    currentLang = btn.dataset.lang;

    // Always update all static UI text immediately
    applyLanguageToUI();

    // Reload playbook content if one is open
    if (currentPlaybookId) {
      loadPlaybook(currentPlaybookId);
    }
  });
});

// ──────────── PLAYBOOK LOADING ────────────
async function loadPlaybook(id) {
  currentPlaybookId = id; // track separately
  switchView("playbook");
  document.getElementById("playbookTitle").textContent = t("loadingPlaybook");
  document.getElementById("playbookSummary").textContent = "";

  let data = null;

  // 1. Try backend API first
  try {
    const res = await fetch(`${API_BASE}/v1/playbooks/${id}?lang=${currentLang}`);
    if (res.ok) {
      data = await res.json();
    }
  } catch (_) { /* API unavailable */ }

  // 2. Fallback: fetch JSON directly (relative to origin root for http.server)
  //    http.server serves prototype/frontend/, so ../../content = VIT Testing/content
  if (!data) {
    const paths = [
      `${CONTENT_BASE}/playbooks/${id}.${currentLang}.json`,
      `${CONTENT_BASE}/playbooks/${id}.en.json`          // English fallback
    ];
    for (const path of paths) {
      try {
        const res = await fetch(path);
        if (res.ok) { data = await res.json(); break; }
      } catch (_) { /* try next */ }
    }
  }

  if (data) {
    renderPlaybook(data);
  } else {
    document.getElementById("playbookTitle").textContent = t("errorPlaybook");
    document.getElementById("playbookSummary").textContent = "";
  }
}

function renderPlaybook(data) {
  currentPlaybook = data;
  // currentPlaybookId is already set in loadPlaybook

  document.getElementById("playbookTitle").textContent   = data.title || "Playbook";
  document.getElementById("playbookSummary").textContent = data.summary_line || "";

  // Re-apply section header translations (may have changed)
  applyLanguageToUI();

  // ── Do Now Steps ──
  const doNowContainer = document.getElementById("doNowList");
  doNowContainer.innerHTML = "";
  (data.do_now || []).forEach((step, idx) => {
    const card = document.createElement("div");
    card.className = "step-card";
    card.innerHTML = `<div class="step-num">${idx + 1}</div><div class="step-text">${step.text}</div>`;
    doNowContainer.appendChild(card);
  });

  // ── Avoid Steps ──
  const avoidContainer = document.getElementById("avoidList");
  avoidContainer.innerHTML = "";
  const avoidSection = document.getElementById("avoidSection");
  if (data.avoid && data.avoid.length) {
    avoidSection.style.display = "block";
    data.avoid.forEach((item, idx) => {
      const card = document.createElement("div");
      card.className = "step-card";
      card.innerHTML = `<div class="step-num">${idx + 1}</div><div class="step-text">${item.text}</div>`;
      avoidContainer.appendChild(card);
    });
  } else {
    avoidSection.style.display = "none";
  }

  // ── Helplines ──
  const helplinesContainer = document.getElementById("whoToCallList");
  helplinesContainer.innerHTML = "";
  (data.who_to_call || []).forEach(num => {
    const a = document.createElement("a");
    a.className = "helpline-btn";
    a.href = `tel:${num}`;
    a.textContent = `📞 ${num}`;
    helplinesContainer.appendChild(a);
  });

  // ── Law Cards ──
  const lawContainer = document.getElementById("lawCardsList");
  lawContainer.innerHTML = "";
  (data.law || []).forEach(l => {
    const item = document.createElement("div");
    item.className = "law-card";
    item.innerHTML = `
      <strong>${l.act} — Section ${l.section}: ${l.heading || ""}</strong>
      <p class="law-quote">"${l.quote}"</p>
      <p class="law-plain">${l.plain_line}</p>
    `;
    lawContainer.appendChild(item);
  });

  // ── Next Steps ──
  const nextContainer = document.getElementById("nextList");
  nextContainer.innerHTML = "";
  const nextSection = document.getElementById("nextSection");
  if (data.next && data.next.length) {
    nextSection.style.display = "block";
    data.next.forEach((item, idx) => {
      const card = document.createElement("div");
      card.className = "step-card";
      card.innerHTML = `<div class="step-num">${idx + 1}</div><div class="step-text">${item.text}</div>`;
      nextContainer.appendChild(card);
    });
  } else {
    nextSection.style.display = "none";
  }

  // ── Officer Card Population ──
  const officerCard = data.officer_card;
  if (officerCard) {
    const lawIds = officerCard.law_ids || [];
    const primaryLaw = (data.law || []).find(l => lawIds.includes(l.section_id)) || data.law?.[0];
    if (primaryLaw) {
      document.getElementById("officerActTitle").textContent = primaryLaw.act;
      document.getElementById("officerSection").textContent  = `Section ${primaryLaw.section}: ${primaryLaw.heading || ""}`;
      document.getElementById("officerVerbatimQuote").textContent = `"${primaryLaw.quote}"`;
    }
    document.getElementById("officerPlainLine").textContent     = officerCard.plain_line || "";
    document.getElementById("officerConsequences").textContent  =
      "Refusal to register an FIR is a criminal offence punishable under BNS Section 198 with rigorous imprisonment.";
  } else if (data.law && data.law.length) {
    const pl = data.law[0];
    document.getElementById("officerActTitle").textContent      = pl.act;
    document.getElementById("officerSection").textContent       = `Section ${pl.section}: ${pl.heading || ""}`;
    document.getElementById("officerVerbatimQuote").textContent = `"${pl.quote}"`;
    document.getElementById("officerPlainLine").textContent     = pl.plain_line;
  }
}

// ──────────── OFFICER CARD TOGGLE ────────────
document.getElementById("showOfficerBtn").addEventListener("click",  () => switchView("officer"));
document.getElementById("closeOfficerBtn").addEventListener("click", () => switchView("playbook"));
document.getElementById("playbookBackBtn").addEventListener("click", () => {
  currentPlaybookId = null;
  currentPlaybook   = null;
  switchView("home");
});
document.getElementById("askBackBtn").addEventListener("click", () => switchView("home"));

// ──────────── SITUATION CARD TAPS ────────────
document.querySelectorAll(".situation-card").forEach(card => {
  card.addEventListener("click", () => {
    const id = card.dataset.id;
    if (id === "fir_refusal") {
      loadPlaybook("fir_refusal");
    } else {
      showToast(`"${card.querySelector("h3")?.textContent}" — ${t("comingSoon")}`);
    }
  });
  card.addEventListener("keydown", e => {
    if (e.key === "Enter" || e.key === " ") card.click();
  });
});

function showToast(msg) {
  const toast = document.createElement("div");
  toast.style.cssText = `
    position:fixed; bottom:90px; left:50%; transform:translateX(-50%);
    background:#1e293b; color:#fff; padding:10px 20px; border-radius:20px;
    font-size:13px; font-weight:600; z-index:9999; white-space:nowrap;
    box-shadow:0 4px 16px rgba(0,0,0,0.3); max-width:90vw; text-align:center;
  `;
  toast.textContent = msg;
  document.body.appendChild(toast);
  setTimeout(() => toast.remove(), 2800);
}

// ──────────── ASK LEGAL QUESTION PIPELINE ────────────
async function handleAsk(queryText) {
  if (!queryText.trim()) return;

  switchView("askResult");
  document.getElementById("qaQuestionText").textContent = queryText;
  document.getElementById("qaSummaryText").textContent  = "";
  document.getElementById("qaQuotesContainer").innerHTML = "";
  document.getElementById("askBadge").className          = "tier-badge";
  document.getElementById("askBadge").textContent        = "";

  const loadingEl = document.getElementById("qaLoadingState");
  // Update loading text in current language
  const loadingP = loadingEl.querySelector("p");
  if (loadingP) loadingP.textContent = t("analysingText");
  loadingEl.classList.add("visible");

  // Update static labels in this view
  const yourQLbl = document.querySelector(".user-q-display strong");
  if (yourQLbl) yourQLbl.textContent = t("yourQuestion");
  const guidanceLbl = document.querySelector(".qa-summary-box strong");
  if (guidanceLbl) guidanceLbl.textContent = t("lawsathiGuidance");
  const backBtn = document.getElementById("askBackBtn");
  if (backBtn) backBtn.textContent = t("back");

  try {
    const res = await fetch(`${API_BASE}/v1/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: queryText, lang: currentLang })
    });
    const result = await res.json();
    loadingEl.classList.remove("visible");

    const badge = document.getElementById("askBadge");
    badge.className = `tier-badge ${result.badge || "not_confirmed"}`;
    const badgeLabels = {
      from_the_law:       "📖 From The Law — Verified",
      not_confirmed:      "⚠️ Not Confirmed",
      emergency_override: "🚨 Emergency — Call 112",
      provider_error:     "⚡ Offline Mode"
    };
    badge.textContent = badgeLabels[result.badge] || result.badge || "Unknown";

    document.getElementById("qaSummaryText").textContent =
      result.answer?.summary || result.message || "No response received.";

    const quotesContainer = document.getElementById("qaQuotesContainer");
    quotesContainer.innerHTML = "";

    if (result.badge === "emergency_override") {
      const emergencyDiv = document.createElement("div");
      emergencyDiv.style.cssText =
        "background:#fee2e2;border:2px solid #dc2626;padding:16px;border-radius:12px;text-align:center;margin-bottom:12px;";
      emergencyDiv.innerHTML = `<strong style="color:#b91c1c;font-size:16px;">🚨 Call 112 NOW if you are in danger</strong>`;
      quotesContainer.prepend(emergencyDiv);
    }

    (result.answer?.quotes || []).forEach(q => {
      const qDiv = document.createElement("div");
      qDiv.className = "quote-result-card";
      qDiv.innerHTML = `
        <div class="qr-meta">${q.act || ""} — Section ${q.section || ""}</div>
        <p class="qr-quote">"${q.quote || ""}"</p>
        ${q.verified ? '<span class="qr-verified">✅ Deterministically Verified Against Official Gazette</span>' : ""}
      `;
      quotesContainer.appendChild(qDiv);
    });

  } catch (err) {
    loadingEl.classList.remove("visible");
    document.getElementById("qaSummaryText").textContent =
      "Unable to reach Q&A service. Please use the offline playbooks or call 112.";
    document.getElementById("askBadge").className  = "tier-badge provider_error";
    document.getElementById("askBadge").textContent = "⚡ Offline Mode";
    console.error("Ask API error:", err);
  }
}

document.getElementById("askBtn").addEventListener("click", () => {
  const query = document.getElementById("queryInput").value;
  handleAsk(query);
});

document.getElementById("queryInput").addEventListener("keydown", e => {
  if (e.key === "Enter") handleAsk(e.target.value);
});

// ──────────── WEB SPEECH RECOGNITION (STT) ────────────
const micBtn   = document.getElementById("micBtn");
const micLabel = document.getElementById("micLabel");

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.continuous     = false;
  recognition.interimResults = false;
  let isListening = false;

  micBtn.addEventListener("click", () => {
    if (isListening) { recognition.stop(); return; }
    recognition.lang = currentLang === "hi" ? "hi-IN"
                     : currentLang === "mr" ? "mr-IN"
                     : "en-IN";
    try {
      recognition.start();
      isListening = true;
      micBtn.classList.add("recording");
      micLabel.dataset.listening = "1";
      micLabel.textContent = t("listening");
    } catch (e) { console.error("STT start error:", e); }
  });

  const resetMic = () => {
    micBtn.classList.remove("recording");
    delete micLabel.dataset.listening;
    micLabel.textContent = t("tapToSpeak");
    isListening = false;
  };

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    document.getElementById("queryInput").value = transcript;
    resetMic();
    handleAsk(transcript);
  };
  recognition.onerror = resetMic;
  recognition.onend   = resetMic;

} else {
  micBtn.style.opacity = "0.45";
  micBtn.style.cursor  = "not-allowed";
  micLabel.textContent = t("voiceUnavailable");
}

// ──────────── WEB SPEECH SYNTHESIS (TTS) ────────────
document.getElementById("playAllAudioBtn").addEventListener("click", () => {
  if (!("speechSynthesis" in window) || !currentPlaybook) return;
  window.speechSynthesis.cancel();

  const steps = (currentPlaybook.do_now || [])
    .map((s, i) => `${i + 1}. ${s.text}`)
    .join(". ");

  const textToSpeak = [
    currentPlaybook.title,
    currentPlaybook.summary_line,
    steps
  ].filter(Boolean).join(". ");

  const utterance  = new SpeechSynthesisUtterance(textToSpeak);
  utterance.lang   = currentLang === "hi" ? "hi-IN"
                   : currentLang === "mr" ? "mr-IN"
                   : "en-US";
  utterance.rate   = 0.95;
  utterance.pitch  = 1;
  window.speechSynthesis.speak(utterance);
});

// ──────────── OFFLINE DETECTION & SERVICE WORKER ────────────
const offlineEl = document.getElementById("offlineIndicator");

function updateOnlineStatus() {
  if (navigator.onLine) {
    offlineEl.classList.remove("visible");
  } else {
    offlineEl.classList.add("visible");
  }
}

window.addEventListener("online",  updateOnlineStatus);
window.addEventListener("offline", updateOnlineStatus);
updateOnlineStatus();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js")
      .then(() => console.log("[LawSathi] Service Worker registered."))
      .catch(err => console.warn("[LawSathi] SW registration failed:", err));
  });
}

// ──────────── INIT ────────────
// Apply default English labels on first load
applyLanguageToUI();
