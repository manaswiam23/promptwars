# CivicBridge: Universal Gemini-Powered Societal Problem Solver
> **PromptWars Hackathon Edition**  
> *Transforming raw, emotional human intent into structured, actionable, and legally sound solutions for complex societal challenges.*

---

## 🌍 The Mission & Problem Statement

Every day, ordinary citizens, vulnerable families, and grassroots communities face high-stakes societal crises:
- **Municipal Water Contamination**: Toxic tap water causing pediatric illness while water boards deflect blame.
- **Illegal Housing Evictions**: Predatory landlords locking gates and cutting power in retaliatory disputes.
- **Arbitrary Healthcare Claim Denials**: Algorithmic insurance rejections for life-saving chemotherapy.
- **Dangerous School Infrastructure**: Falling concrete and live electrical wires threatening elementary students.
- **Labor Exploitation & Wage Theft**: Sub-contractors withholding wages from migrant workers with threats of blacklisting.

### The Intent-to-Execution Chasm
Citizens express their crises **emotionally, colloquially, and in natural human speech**:  
> *"Our tap water smells like rotten eggs and our kids are in the hospital. The city won't answer."*

Societal institutions demand **formal statutory jurisdictions, regulatory citations, procedural evidence, and legal demand letters**:  
> *Statutory Notice under Section 18 of Public Health Act served to the Municipal Commissioner with certified proof of delivery.*

**CivicBridge acts as the universal cognitive bridge** between this raw human intent and complex institutional machinery.

---

## 🏛️ System Architecture

```
                                  [ Human Intent ]
                     (Voice / Spoken Audio / Colloquial Text / Photos)
                                         │
                                         ▼
                 ┌─────────────────────────────────────────────────┐
                 │        Step 1: Empathic Intent Ingestion        │
                 │  - Voice Recognition (Web Speech API)           │
                 │  - Multimodal Evidence Attachment Preview       │
                 │  - Emotional Tone & Vulnerability Mapping       │
                 └───────────────────────┬─────────────────────────┘
                                         │
                                         ▼
                 ┌─────────────────────────────────────────────────┐
                 │     Step 2: The Cognitive Bridge (Gemini)       │
                 │  - Core Problem & Statutory Domain Classifier   │
                 │  - Competent Jurisdiction & Legal Body Finder   │
                 │  - Statutory Framework & Directive Retrieval    │
                 │  - Root Cause Analysis                          │
                 └───────────────────────┬─────────────────────────┘
                                         │
                                         ▼
                 ┌─────────────────────────────────────────────────┐
                 │   Step 3: Strategy Forge ("PromptWars" Engine)  │
                 │  - Simulates 3 Competing Resolution Pathways:   │
                 │      * Route Alpha: Direct Administrative Notice│
                 │      * Route Beta: Regulatory Ombudsman Injunction│
                 │      * Route Gamma: Collective Sunshine Campaign│
                 │  - Pits routes on Speed, Success %, Risk & Cost │
                 │  - Issues Strategic Verdict                     │
                 └───────────────────────┬─────────────────────────┘
                                         │
                                         ▼
                 ┌─────────────────────────────────────────────────┐
                 │      Step 4: Bureaucratic Artifact Synthesizer  │
                 │  - Ready-to-Serve Formal Statutory Notice       │
                 │  - FOIA / Right to Information Disclosure Brief │
                 │  - Sequential Evidence Collection Checklist     │
                 │  - 1-Click Clipboard Copy & PDF Print/Export    │
                 └───────────────────────┬─────────────────────────┘
                                         │
                                         ▼
                 ┌─────────────────────────────────────────────────┐
                 │      Step 5: Civic Advocate Co-Pilot (Chat)     │
                 │  - Interactive AI Caseworker guiding citizen    │
                 │  - Tactical advice on anti-retaliation, dates,  │
                 │    evidence defense, and pro se filing          │
                 └─────────────────────────────────────────────────┘
```

---

## 🚀 Key Features

1. **Voice & Plain-Language Ingestion**:
   - Built-in microphone voice transcription via Web Speech API.
   - Accepts raw, unorganized, emotional stories without legal jargon.
2. **Preset Real-World Societal Crises (1-Click Test)**:
   - Contaminated Municipal Water Crisis
   - Unlawful Retaliatory Eviction
   - Arbitrary Cancer Care Claim Denial
   - Elementary School Hazard Neglect
   - Construction Contractor Wage Theft
3. **The Strategy Forge ("PromptWars")**:
   - Pits 3 distinct strategic avenues against each other.
   - Evaluates timeline, success rate %, risk level, and resource demands side-by-side.
4. **Actionable Civic & Legal Instruments**:
   - Formal Legal / Grievance Notice citing exact statutes and setting strict cure deadlines.
   - Official FOIA / RTI disclosure application to compel public records.
   - Comprehensive Evidence Checklist with practical gathering instructions.
   - 1-click **Export to PDF** or copy to clipboard.
5. **Civic Advocate Co-Pilot**:
   - Conversational AI guide specialized in civil rights and bureaucratic casework.
   - Real-time advice on anti-retaliation protections and self-representation.
7. **Intent-to-Action Bridge Engine (Multimodal Emergency & Decision System)**:
   - Full 5-step cognitive pipeline: **PARSE ➔ FUSE ➔ VERIFY ➔ STRUCTURE ➔ ACT**.
   - **Emergency Multimedia Module**: Auto-triggers on fire, cardiac/medical collapse, highway rollover, assault/intrusion.
   - **Degraded-Media Signal Extraction**: Extracts partial cues from blurry photos, dark video, and noisy audio with confidence ratings.
   - **Contradiction Resolution**: When streams conflict (e.g. video shows raging flames but caller says "small fire"), defaults fail-safe to Critical urgency.
   - **Medical Context Tie-In**: Auto-surfaces allergies (e.g. penicillin anaphylaxis) and medications/conditions from messy records into responder packets.
   - **Parallel Authority Dispatch & Low-Bandwidth SMS Fallback**: Routes simultaneously to Fire, Police, and EMS, notifies personal contacts, and generates lightweight SMS alert strings.
   - **Accessibility**: Single-Tap "Something's Wrong" mode (elderly/fall protocol) and Silent SOS mode (deaf/mute/covert intrusion).
   - **Streamlit Frontend Dashboard**: Interactive, real-time command center located at `streamlit_app.py`.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.13, FastAPI, Uvicorn, Pydantic v2
- **Frontend Interfaces**:
  - **Streamlit Interactive Operations Dashboard** (`streamlit_app.py`)
  - Single-Page Application (SPA) (`app/static/index.html` with Tailwind CSS)
- **AI Engine**: Google Gemini API (`google-generativeai` / `gemini-2.5-flash` / `gemini-1.5-flash`) + High-Fidelity Cognitive Simulation

---

## 📦 Quick Start Guide

### 1. Install Dependencies
```bash
py -3.13 -m pip install -r requirements.txt
```

### 2. Configure API Key (Optional)
Copy `.env.example` to `.env` and set your key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If no key is set, the system automatically runs in high-fidelity simulated mode with all features and presets active).*

### 3. Run the Streamlit Interface (Intent-to-Action Dashboard)
```bash
py -3.13 -m streamlit run streamlit_app.py --server.port 8501
```
Open **`http://localhost:8501`** in your browser.

### 4. Run the FastAPI Backend Server
```bash
py -3.13 run.py
```
Or with uvicorn directly:
```bash
py -3.13 -m uvicorn app.main:app --reload --port 8000
```
Open **`http://localhost:8000`** for the SPA or **`http://localhost:8000/docs`** for the interactive Swagger API documentation.


---

## 🧪 Running Automated Tests

Run the test suite to verify all endpoints, presets, and AI pipeline models:
```bash
py -3.13 -m pytest tests/test_api.py -v
```

---

## 🏆 Societal Impact

CivicBridge breaks down the asymmetric knowledge barrier that prevents ordinary citizens from holding powerful entities accountable. By bridging human emotion into enforceable administrative instruments, it democratizes access to justice and public accountability.
