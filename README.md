# ⚖️ LawSathi Prototype — Run & Test Guide

> **Pre-Hackathon Prototype** for VIT CODE APEX 3.0 (Track 3: Open Innovation)  
> Voice-First, Offline-Capable Citizen Legal Aid & Police Encounter Companion.

---

## 📌 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (PWA / Vanilla JS)       http://localhost:3000    │
│  • Voice STT / TTS                • Show-to-Officer Card   │
│  • Offline Service Worker         • Multilingual UI        │
└──────────────────────────────┬──────────────────────────────┘
                               │ JSON / HTTP
┌──────────────────────────────▼──────────────────────────────┐
│  Backend (FastAPI)                 http://localhost:8000    │
│  • Safety Router (112 Trap)       • Quote-Verification Guard│
│  • In-Memory Corpus (BNSS/BNS)    • Mock Mode / Gemini Live │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (Running the Prototype)

Run the backend and frontend in **two separate terminal windows**.

### Terminal 1: Backend Server (FastAPI on Port 8000)

#### PowerShell (Windows):
```powershell
cd "prototype\backend"

# (Optional) Set your Gemini API key for live generation.
# If omitted, backend automatically runs in Grounded Mock Mode.
# $env:GEMINI_API_KEY="your-gemini-api-key"

# Activate virtual environment
.\venv\Scripts\activate

# Start the server with hot reload
uvicorn prototype_server:app --reload --port 8000
```

#### Command Prompt (cmd.exe):
```cmd
cd prototype\backend
venv\Scripts\activate.bat
uvicorn prototype_server:app --reload --port 8000
```

#### Bash / macOS / Linux:
```bash
cd prototype/backend
source venv/bin/activate
uvicorn prototype_server:app --reload --port 8000
```

---

### Terminal 2: Frontend Client (Static Server on Port 3000)

#### PowerShell / CMD / Bash:
```powershell
cd "prototype\frontend"

# Serve via Python's built-in HTTP server
python -m http.server 3000
```

---

## 🌐 URLs & Endpoints

| Component | URL | Description |
|---|---|---|
| **Web Application** | [http://localhost:3000](http://localhost:3000) | Citizen crisis interface (PWA) |
| **API Swagger UI** | [http://localhost:8000/docs](http://localhost:8000/docs) | Interactive OpenAPI documentation |
| **API ReDoc** | [http://localhost:8000/redoc](http://localhost:8000/redoc) | Alternative API documentation |
| **API Health Check** | [http://localhost:8000/health](http://localhost:8000/health) | Server status and corpus chunk count |

---

## 🛠️ First-Time Setup (If Reinstalling)

If you clone on a new machine or recreate the environment:

```powershell
cd "prototype\backend"
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Dependencies (`requirements.txt`):
- `fastapi` — Asynchronous REST API
- `uvicorn` — ASGI server
- `httpx` — Async HTTP client for LLM providers
- `pydantic` — Data validation & request schemas
- `python-dotenv` — Environment configuration

---

## 🧪 Quick API Verification Commands

Test that the backend is responding properly via PowerShell:

### 1. Health Check
```powershell
curl http://localhost:8000/health
```
**Expected Response:**
```json
{"status":"ok","corpus_chunks":4,"gemini_configured":false}
```

### 2. Helplines Endpoint
```powershell
curl http://localhost:8000/v1/helplines
```

### 3. Fetch FIR Refusal Playbook (English / Hindi / Marathi)
```powershell
curl "http://localhost:8000/v1/playbooks/fir_refusal?lang=en"
curl "http://localhost:8000/v1/playbooks/fir_refusal?lang=hi"
curl "http://localhost:8000/v1/playbooks/fir_refusal?lang=mr"
```

### 4. Safety Router Test (Emergency Intercept)
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/v1/ask" -Method Post -ContentType "application/json" -Body '{"question": "someone is attacking me with knife", "lang": "en"}' | ConvertTo-Json -Depth 5
```
*Bypasses LLM, immediately returns 112 emergency routing.*

### 5. Grounded Legal Question (BNSS 173 Quote Guard)
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/v1/ask" -Method Post -ContentType "application/json" -Body '{"question": "can police refuse to file fir", "lang": "en"}' | ConvertTo-Json -Depth 5
```
*Returns Tier 2 verified quote with official Section 173 BNSS text.*

---

## 🎯 5 Core Prototype Validation Scenarios

1. **Grounded Legal Q&A (Tier 2):**
   - In the frontend input box or via mic, ask: `"Can police refuse my FIR?"`
   - **Expectation:** Green `📖 From The Law` badge, verbatim Section 173 BNSS citation, and plain-language explanation.
2. **Safety Router Trigger (Tier 3 Emergency Override):**
   - Type or speak: `"Someone is attacking me right now"` or `"I want to harm myself"`
   - **Expectation:** Immediate high-priority red alert with direct tap-to-call `112` button; LLM call bypassed.
3. **Hallucination Hard Refusal (Tier 3 Guard):**
   - Ask an unsupported topic: `"Can police seize my crypto wallet?"`
   - **Expectation:** Amber `⚠️ Not Confirmed from Law` notice advising verified playbook consultation or helpline contact without hallucinating non-existent laws.
4. **Show-to-Officer High-Contrast Card:**
   - Tap on the **Police Refusing FIR** card, then click **"👮 Show This to the Police Officer"**.
   - **Expectation:** High-contrast dark full-screen display of BNSS Section 173 with official statutory consequences under BNS Section 198.
5. **Offline PWA & Airplane Mode:**
   - Open [http://localhost:3000](http://localhost:3000), let the service worker cache assets, then disconnect your internet.
   - Refresh the page and open the FIR refusal playbook.
   - **Expectation:** "⚡ Offline Mode" indicator appears; playbooks and officer cards function completely offline.

---

## 🔧 Troubleshooting

- **Microphone not working:** Use **Google Chrome** or **Microsoft Edge**. Web Speech Recognition requires browser permissions and an active microphone.
- **Port 8000 or 3000 already in use:**
  - For backend: change port with `--port 8001` (and update `API_BASE` in `prototype/frontend/app.js`).
  - For frontend: run `python -m http.server 3001`.
- **CORS Issues:** `prototype_server.py` has `CORSMiddleware` configured with `allow_origins=["*"]` by default.
