# FinlyAI — Autonomous Virtual CFO for SMEs

**Takeover Hackathon 2026 Submission**

FinlyAI is an autonomous financial management agent that acts as a virtual Chief Financial Officer (CFO) for small and medium enterprises (SMEs). It continuously monitors inventory, automates purchase order billing, and runs AI-driven cash flow analysis — giving small businesses executive-level financial clarity without the cost of a full-time finance team.

Unlike simple simulations, this is a real-world automation workflow that connects local CSV stock records, generates professional PDFs, drafts vendor notification emails, runs live predictive analysis via **Google Gemini API**, and maintains an immutable audit trail using a local SQLite database.

---

## System Architecture

FinlyAI uses a modular **"Fragments"** architecture, allowing each step in the workflow to run independently, handle errors gracefully, and be tested in isolation.

```
┌────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
│       FRAGMENT 1       │      │       FRAGMENT 2        │      │       FRAGMENT 3        │
│   Inventory Tracker    │ ───▶ │    Automated Billing    │ ───▶ │   AI Virtual CFO Agent  │
│  (inventory.py)        │      │     (billing.py)        │      │       (cfo.py)          │
└───────────┬────────────┘      └────────────┬────────────┘      └────────────┬────────────┘
            │                                │                                │
            │                                │                                │
            └────────────────────────────────┼────────────────────────────────┘
                                             ▼
                                ┌─────────────────────────┐
                                │   SQLite Audit Trail    │
                                │      (finlyai.db)       │
                                └─────────────────────────┘
```

| Fragment | Module | Input | Output / Action |
|---|---|---|---|
| **1. Inventory Tracker** | `inventory.py` | `inventory.csv` | Parses stock data, monitors thresholds, and raises structured low-stock alerts. |
| **2. Automated Billing** | `billing.py` | Low-stock alerts | Generates professional PO PDFs in `output_pos/` (ReportLab) & drafts reorder emails (smtplib dry-run). |
| **3. AI Virtual CFO Agent** | `cfo.py` | Pending POs & cash position | Calls Google Gemini (`gemini-2.5-flash` model) to return structured JSON recommendations (Approve/Hold, reasoning, risk). |

---

## Tech Stack

- **Core Engine**: Python 3.9+
- **Database (Audit Trail)**: SQLite (`sqlite3`)
- **AI Analytics**: Google Gemini API (`gemini-2.5-flash` model) via the `google-genai` Python SDK
- **PDF Generation**: ReportLab
- **Workflow Scheduler**: `schedule`
- **Environment Management**: `python-dotenv`
- **Unit Testing**: `unittest`

---

## Getting Started

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Installation
Clone the repository (or extract the project) and install the python dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Copy the example environment file to `.env`:
```bash
cp .env.example .env
```
Open `.env` and configure the following variables:
- `GEMINI_API_KEY`: Your Google Gemini API Key. If left empty, FinlyAI automatically runs in **Mock Mode** using a local deterministic financial reasoning rule engine.
- `SCHEDULE_INTERVAL_MINUTES`: Frequency at which the automated pipeline executes when running in scheduled mode (default: `5.0`).

---

## Running FinlyAI

### Run the Pipeline Once (Manual Mode)
To trigger a manual, one-off execution of the pipeline:
```bash
python main.py
```
*Depending on whether `GEMINI_API_KEY` is present in `.env`, the script will print either a `[MOCK MODE - no API key set]` notice or run live API analysis.*

### Run the Pipeline on a Loop (Schedule Mode)
To run the autonomous CFO agent in the background on a periodic loop:
```bash
python main.py --schedule
```
*This reads the interval frequency from your `.env` (or defaults to 5 minutes).*

### Check Audit History
FinlyAI records every execution status, low stock alert count, draft PO count, and the CFO JSON decision to a local SQLite database (`finlyai.db`). To review the history via the CLI:
```bash
python main.py --history
```

---

## Running Unit Tests

The codebase includes a suite of automated unit tests covering inventory threshold detection, PDF generation, and email body drafting. Run them with:
```bash
python -m unittest test_finlyai.py
```

---

## Demo Files
- `finlyai_dashboard.html`: A premium visual dashboard mockup showcasing the "Fragments" architecture and ledger logs.
- `inventory.csv`: Realistic SME inventory database file.
"# FinlyAI-CFO-Agent" 
