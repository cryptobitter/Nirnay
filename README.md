# ⚖️ Nirnay

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Claude](https://img.shields.io/badge/Claude-Sonnet%205-D97757?logo=anthropic&logoColor=white)](https://www.anthropic.com/)
[![LlamaIndex](https://img.shields.io/badge/RAG-LlamaIndex-purple)](https://www.llamaindex.ai/)
[![ChromaDB](https://img.shields.io/badge/VectorDB-Chroma-1E90FF)](https://www.trychroma.com/)
[![Solidity](https://img.shields.io/badge/Solidity-Smart%20Contract-363636?logo=solidity&logoColor=white)](https://soliditylang.org/)
[![Polygon](https://img.shields.io/badge/Blockchain-Polygon%20Amoy-8247E5?logo=polygon&logoColor=white)](https://polygon.technology/)
[![Postgres](https://img.shields.io/badge/Database-Supabase%20Postgres-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com/)
[![JWT](https://img.shields.io/badge/Auth-JWT-black?logo=jsonwebtokens&logoColor=white)](https://jwt.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](#-license)

**An AI-powered policy Q&A system that answers institutional compliance questions with cited evidence — and permanently anchors every decision to a public blockchain, so the audit trail is independently verifiable by anyone, not just trusted on the institution's word.**

Built as a hackathon project combining **Retrieval-Augmented Generation**, **rule-based policy auditing**, and **blockchain-anchored tamper-evidence**.

> Pramaan verifies that a record is genuine. Nirnay verifies that a decision was never altered.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#️-tech-stack)
- [System Pipeline](#-system-pipeline)
- [Trust & Verification Model](#-trust--verification-model)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Application Pages](#️-application-pages)
- [Project Task Tracker](#-project-task-tracker)
- [Quality Assurance & Bug Fixes](#-quality-assurance--bug-fixes)
- [Competitive Landscape](#-competitive-landscape)
- [Known Limitations](#️-known-limitations)
- [License](#-license)

---

## 🧭 Overview

Institutions — colleges, startup compliance teams, audit functions — make policy-based decisions constantly (scholarship eligibility, vendor compliance, regulatory checks), but the process is slow (manual document search) and unauditable (decisions live in emails or memory, with no tamper-proof record). Existing tools that solve tamper-evident AI audit trails (Polygraf AI, OriginStamp) target large enterprises using private, vendor-controlled logging — leaving smaller institutions with no affordable, independently verifiable option.

**Nirnay** answers policy questions from an institution's own documents using RAG + an LLM, routes each answer through a lightweight rule-based policy engine (approve / flag / escalate), and permanently hashes every decision record onto a public blockchain testnet — so the tamper-evidence claim is provable by anyone with the record ID, not just asserted by the institution running the software.

## ✨ Features

- 📄 **Document Ingestion** — upload institutional PDFs (policies, contracts, regulations); text is extracted, chunked, embedded, and indexed per institution
- 💬 **Cited Q&A** — ask questions in plain language, get answers grounded only in the institution's own documents, with source document + page citations and a confidence score
- ⚖️ **Policy Engine** — deterministic rule-based decisioning: low confidence escalates for human review, sensitive keywords (data sharing, termination, penalty, liability, etc.) get flagged, everything else is auto-approved
- 🔒 **Strict Per-Institution Isolation** — each institution's documents live in a separate vector store collection by construction, not just by filter logic, so one institution's policies can never leak into another's answers
- 🔗 **Blockchain-Anchored Audit Trail** — every decision (question, answer, evidence, confidence, outcome) is deterministically hashed (SHA-256) and the hash is written to a smart contract on the Polygon Amoy testnet
- 🌍 **Public Verification** — anyone, with no account, can paste a record ID and independently confirm a decision record hasn't been altered since it was made — the audit trail doesn't require trusting the institution
- 🧑‍🤝‍🧑 **Role-Based Access** — staff see only their own question history; admins see the full institutional audit log
- ⏳ **Institution Verification Gating** — new institutions start `pending`; document upload and Q&A are blocked until an institution is marked `verified`

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| 🧠 RAG Framework | LlamaIndex (chunking, indexing, retrieval) |
| 🗂️ Vector Store | ChromaDB — one isolated collection per institution |
| 🔡 Embeddings | OpenAI `text-embedding-3-small` |
| 🤖 LLM | Claude API (`claude-sonnet-5`) — cited answer + confidence synthesis |
| ⚙️ Backend | Python, FastAPI |
| 🗄️ Database | Supabase (Postgres) via SQLAlchemy |
| 🔐 Auth | JWT (bcrypt-hashed passwords via passlib) |
| 🔗 Blockchain | Solidity smart contract on Polygon Amoy testnet |
| 🌉 Chain Integration | web3.py |
| #️⃣ Hashing | Python `hashlib` — deterministic SHA-256 |
| 🎨 Frontend | React (Stitch-generated screens) |

## 🔄 System Pipeline

```
flowchart TD
    A[📄 Document Upload] --> B[✂️ Chunking - LlamaIndex]
    B --> C[🔡 Embedding - OpenAI]
    C --> D[🗂️ Chroma Collection, per institution]
    E[❓ User Question] --> F[🔎 Top-k Retrieval, same institution collection]
    D --> F
    F --> G[🤖 Claude - cited answer + confidence]
    G --> H[⚖️ Policy Engine - approve / flag / escalate]
    H --> I[🗄️ Save to Postgres]
    I --> J[#️⃣ Deterministic SHA-256 Hash]
    J --> K[🔗 Hash written to Solidity contract]
    K --> L[🌍 Publicly verifiable by record ID, no login]
```

## 🔐 Trust & Verification Model

The tamper-evidence claim only means something if it's checkable independently — so verification is built as a standalone, public, zero-trust flow.

```
flowchart LR
    A[Assessment Created] --> B[Hash computed from full record incl. sources]
    B --> C[Hash saved to Postgres]
    B --> D[Hash submitted to smart contract]
    E[Anyone requests /verify/id] --> F[Record re-hashed from current DB state]
    F --> G{Matches stored hash?}
    G -->|No| H[❌ TAMPERING DETECTED]
    G -->|Yes| I{Exists on-chain?}
    I -->|No| J[⚠️ UNANCHORED RECORD]
    I -->|Yes| K[✅ AUTHENTIC - matches on-chain ledger]
```

- The **same shared function** (`build_hash_payload_from_assessment`) builds the hash input both when a record is first created and when it's later re-verified — this guarantees the two can never accidentally drift apart due to inconsistent field formatting (a bug caught and fixed during development — see [Quality Assurance](#-quality-assurance--bug-fixes)).
- Verification is available with **no login** — an auditor, journalist, or student doesn't need an account or institutional trust to confirm a record is authentic.
- Cited **evidence (`sources`) is included in the hash**, not just the answer text — so the citations backing a decision can't be swapped out after the fact without detection.

## 📁 Project Structure

```
nirnay/
├── frontend/                        # React (Stitch-generated) screens
│   └── src/pages/                   # landing, login, signup, pending-verification,
│                                     # upload, ask, history, audit-log, verify
├── backend/
│   ├── main.py                      # FastAPI entrypoint, router mounting, CORS
│   ├── config.py                    # Centralized env-based settings
│   ├── database/
│   │   ├── models.py                # User, Institution, Document, Assessment (SQLAlchemy)
│   │   ├── schema.sql                # Postgres schema (CheckConstraints, UNIQUE record_hash)
│   │   └── db.py                    # Engine/session setup
│   ├── models/
│   │   └── schemas.py               # Pydantic request/response models
│   ├── routers/
│   │   ├── auth.py                  # Signup/login, JWT, pending-verification gating
│   │   ├── documents.py             # Upload + list, institution-scoped
│   │   ├── qa.py                    # RAG → LLM → policy engine → hash → blockchain
│   │   ├── history.py               # Per-user assessment history
│   │   ├── audit.py                 # Full institutional audit log (admin-only)
│   │   └── verify.py                # Public, no-auth verification endpoint
│   └── services/
│       ├── ingestion.py             # PDF extraction + chunking + per-institution indexing
│       ├── embeddings.py            # OpenAI embedding model (single provider, no silent fallback)
│       ├── rag_retrieval.py         # Top-k retrieval, institution-scoped
│       ├── llm_service.py           # Claude prompt construction + cited answer synthesis
│       ├── policy_engine.py         # Rule-based approve / flag / escalate logic
│       ├── hasher.py                # Deterministic SHA-256 hashing (shared payload builder)
│       └── blockchain_service.py    # web3.py — submit/verify hash on Polygon Amoy
├── blockchain/
│   └── contracts/
│       └── NirnayRegistry.sol       # recordHash → (timestamp, submitter) mapping
├── vectorstore/                     # Chroma persistent storage (gitignored)
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Supabase project (free tier) for Postgres
- An OpenAI API key (embeddings) and an Anthropic API key (Claude)
- A throwaway wallet + free Polygon Amoy testnet MATIC (for blockchain writes)

### Clone the repository

```bash
git clone https://github.com/cryptobitter/Nirnay.git
cd Nirnay
```

### Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # Mac/Linux

pip install fastapi uvicorn[standard] python-dotenv pydantic pydantic-settings sqlalchemy psycopg2-binary supabase python-jose[cryptography] passlib[bcrypt] python-multipart pypdf llama-index llama-index-vector-stores-chroma chromadb openai anthropic web3 pytest httpx

# Copy .env.example to .env and fill in your Supabase, OpenAI, Anthropic, and Polygon Amoy credentials
copy .env.example .env

# Run schema.sql against your Supabase project (via the SQL editor), then:
uvicorn main:app --reload
```

### Blockchain setup

```bash
cd blockchain
npm install --save-dev hardhat
npm install @openzeppelin/contracts dotenv
npx hardhat run scripts/deploy.js --network amoy
```

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Open the frontend dev server with the backend running at `http://localhost:8000`. Sign up to create a new institution account — new institutions start `pending` and require manual verification before document upload and Q&A are enabled.

## 🖥️ Application Pages

| Page | Purpose | Status |
|---|---|---|
| 🏠 Landing | Product overview and pitch | ✅ Designed |
| 🔐 Login | Auth against the backend | ✅ Designed |
| 📝 Signup | Create an account, join or create an institution | ✅ Designed |
| ⏳ Pending Verification | Post-signup state while institution is unverified | ✅ Designed |
| 📄 Document Upload | Upload and view institution policy documents | ✅ Designed |
| 💬 Ask a Question | Cited Q&A with confidence + decision status | ✅ Designed |
| 📜 History | Your own past questions and answers | ✅ Designed |
| 🗂️ Audit Log | Full institutional record (admin-only) | ✅ Designed |
| 🌍 Public Verification | Verify any record by ID — no login required | ✅ Designed |

## ✅ Project Task Tracker

### Backend Core

| Task | Status |
|---|---|
| FastAPI app structure, config, CORS | ✅ Done |
| Postgres schema (Users, Institutions, Documents, Assessments) | ✅ Done |
| JWT auth — signup, login, role-based access | ✅ Done |
| Institution pending-verification gating (signup, login, upload, Q&A) | ✅ Done |
| Document upload + per-institution listing | ✅ Done |

### RAG Pipeline

| Task | Status |
|---|---|
| PDF ingestion + sentence-aware chunking | ✅ Done |
| Per-institution vector isolation (Chroma) | ✅ Done |
| Top-k retrieval scoped to institution | ✅ Done |
| Claude-powered cited answer + confidence synthesis | ✅ Done |

### Policy Engine & Trust Layer

| Task | Status |
|---|---|
| Rule-based approve / flag / escalate logic | ✅ Done |
| Deterministic record hashing (SHA-256, includes evidence) | ✅ Done |
| Blockchain submission service (web3.py, mock + real modes) | ✅ Done |
| Public, no-auth verification endpoint | ✅ Done |
| Personal history + institutional audit log (role-scoped) | ✅ Done |

### Blockchain

| Task | Status |
|---|---|
| Solidity contract (`submitRecord` / `getRecord`) | ⬜ Not started |
| Deploy to Polygon Amoy testnet | ⬜ Not started |
| Wire real contract address into backend | ⬜ Not started |

### Frontend

| Task | Status |
|---|---|
| All 9 screens designed (Stitch) | ✅ Done |
| Wire screens to live backend endpoints | ⬜ Not started |

---

## 🔧 Quality Assurance & Bug Fixes

A structured review pass (Gemini generates → Claude reviews → Gemini corrects) was run on every backend file before integration. Documented here for transparency:

| Issue | Severity | Fix |
|---|---|---|
| **Collection-naming mismatch** between ingestion and retrieval — documents were indexed into per-institution collections, but retrieval queried a shared collection nothing wrote to | 🔴 Critical | Unified collection naming (`policy_documents_{institution_id}`) across both files; retrieval now always finds what ingestion actually wrote |
| **`record_hash=""` placeholder violated its own `UNIQUE` constraint** — the second assessment ever created would crash the whole endpoint | 🔴 Critical | Switched to a UUID-based unique placeholder during `flush()`, real hash computed and set before the single final `commit()` |
| **Hash/verification drift risk** — `qa.py` and `verify.py` each built the hash input dict manually, risking silent field-formatting mismatches (e.g. timestamp as string vs. datetime) that would falsely flag untampered records as tampered | 🔴 Critical | Extracted a single shared `build_hash_payload_from_assessment()` used by both creation and verification paths |
| **Silent embedding-model fallback** — missing OpenAI key silently switched to a different embedding model with a different vector dimension, which would have corrupted Chroma similarity search | 🟠 Bug | Removed the fallback; now raises a clear error instead of silently switching providers |
| **`sources` (cited evidence) excluded from the hash** — decision evidence could be altered after the fact without being detected by verification | 🟠 Bug | Added `sources` to the canonical hash payload |
| **Mock blockchain verification always returned `exists: True`** regardless of the hash checked — would have made the entire tamper-detection demo non-functional before a real contract was deployed | 🟠 Bug | Mock mode now uses an in-memory store that actually tracks submitted hashes and correctly rejects unknown ones |
| **`CORS allow_origins=["*"]` combined with `allow_credentials=True`** — invalid per spec, browsers silently reject credentialed requests under this combination | 🟠 Bug | Replaced with an explicit frontend origin allowlist |
| Client-supplied `role` trusted directly on signup — anyone could self-assign `admin` | 🟠 Security | Role hardcoded to `"staff"` server-side on every signup |
| Pending-institution status inferred from "was this institution just created" rather than an actual `status` field — only blocked the *first* signup per institution, not subsequent ones | 🟡 Bug | Added a real `status` column with a `CheckConstraint`; both signup and login now check it explicitly |
| Blockchain submission failures returned a fake string resembling a transaction hash | 🟡 Bug | Real failures now raise `RuntimeError`, caught by the caller and stored as `chain_tx_hash=None` (pending anchor) instead of a misleading fake value |
| Outdated LLM model string | 🟢 Cleanup | Updated to `claude-sonnet-5` |
| Institution name matching was case-sensitive/exact, risking duplicate institution rows | 🟢 Cleanup | Normalized via `.ilike()` + `.strip()` |

## 🏆 Competitive Landscape

Individual components here (RAG, cited answers, tamper-evident logging) all exist elsewhere — most notably **Polygraf AI** (hash-chained AI decision logging) and **OriginStamp/OriginVault** (blockchain-timestamped AI audit trails). Both target large, regulated enterprises using **private or permissioned** logging.

Nirnay's differentiation is specific, not a claim of inventing the underlying technique:
- **Public testnet, not a private ledger** — verification doesn't require trusting the vendor or the institution; anyone can independently check a record
- **Built for small institutions**, not enterprise/government budgets
- **Positioned as a sibling to Pramaan** (credential verification) — one coherent trust-verification philosophy extended from static records to live decisions

## ⚠️ Known Limitations

- No signup path currently creates an `admin` or `reviewer` account — every signup is hardcoded to `role="staff"` to prevent client-side privilege escalation. Promoting a user to `admin` currently requires a manual edit in the Supabase table editor.
- Policy engine keyword-flagging uses plain substring matching on a fixed list — it won't catch every real-world phrasing of a sensitive term, only the exact words configured.
- `assessments.institution_id` currently cascades on institution deletion — acceptable for a demo, but a production version should prevent an audit trail from being deletable at all.
- The Solidity smart contract has not yet been deployed; `blockchain_service.py` runs in a functioning mock mode (in-memory hash tracking) until a real contract address is configured.
- No automated test suite yet — verification of correctness has been manual and via structured code review, not unit/integration tests.

## 📄 License

This project is licensed under the MIT License — see the LICENSE file for details.

---

**Author:** Aditya · Sibling project to [Pramaan](#)
