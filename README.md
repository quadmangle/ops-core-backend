# OPS Core Secure Backend

A secure, compliance-ready backend scaffold built with FastAPI and PostgreSQL, aligned to NIST SP 800-171 and OPS Core security standards.

---

## 🚀 Quick Start

### 1. Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/ops-core-backend.git
cd ops-core-backend/backend
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file:
```env
SECRET_KEY=your_super_secret_key
DATABASE_URL=postgresql://user:password@localhost:5432/ops_core_db
```

### 5. Run the App
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Access API Docs
Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔒 Security Features
- JWT-based Authentication (Zero Trust model ready)
- Role-Based Access Control (RBAC)
- Row-Level Security (PostgreSQL)
- Pre-commit DevSecOps hooks (Bandit, Black, Detect-Secrets)

---

## 📂 Project Structure
```
backend/
├── app/
│   ├── main.py
│   ├── routes/
│   ├── models.py
│   └── security.py
├── db/
│   └── schema.sql
├── .env
├── requirements.txt
├── .gitignore
└── .pre-commit-config.yaml
```

---

## ✅ Compliance Notes
- Framework aligns with NIST 800-171 Controls: AC, IA, AU, SC
- Designed for extensibility into TinyML/LLM and secure microservices

---

## 🛠 Recommended Tools
- **PostgreSQL 13+** with RLS enabled
- **Docker** (optional for local DB container)
- **Alembic** (optional for DB migrations)

---

## 🧠 Contributors
Built and maintained by [Ignite00G]
