# Hospital Patient Management System

A complete backend-focused Hospital Patient Management System built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Streamlit**, and **Uvicorn**.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Frontend | Streamlit |
| Server | Uvicorn |
| Auth | JWT (python-jose) + bcrypt |

---

## ✨ Features

- ✅ **Patient Registration** – Create, read, update, delete patient records
- ✅ **Appointment Scheduling** – Book and manage patient–doctor appointments
- ✅ **Doctor Diagnosis Updates** – Record and update diagnoses and prescriptions
- ✅ **Billing Management** – Generate bills and track payment status
- ✅ **Role-Based Access Control** – Admin / Doctor / Receptionist roles
- ✅ **JWT Authentication** – Secure token-based login
- ✅ **Pydantic Input Validation** – Clean, validated request/response schemas
- ✅ **Swagger UI** – Auto-generated interactive API docs at `/docs`
- ✅ **Streamlit Frontend** – Interactive UI that communicates with the FastAPI backend

---

## 🗂 Project Structure

```
hospital_patient_management_system/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy engine & session
│   ├── auth/
│   │   └── auth.py          # JWT helpers, password hashing, role guards
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── appointment.py
│   │   ├── diagnosis.py
│   │   └── billing.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── user.py
│   │   ├── patient.py
│   │   ├── doctor.py
│   │   ├── appointment.py
│   │   ├── diagnosis.py
│   │   └── billing.py
│   └── routes/              # FastAPI routers
│       ├── auth.py
│       ├── patients.py
│       ├── doctors.py
│       ├── appointments.py
│       ├── diagnosis.py
│       └── billing.py
├── frontend/
│   └── app.py               # Streamlit UI
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone & install dependencies

```bash
git clone <repo-url>
cd hospital_patient_management_system
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and set your PostgreSQL credentials and a secure SECRET_KEY
```

### 3. Set up PostgreSQL

```sql
CREATE DATABASE hospital_db;
```

### 4. Run the FastAPI backend

```bash
uvicorn backend.main:app --reload
```

The API will be live at **http://localhost:8000**.  
Swagger docs: **http://localhost:8000/docs**

### 5. Run the Streamlit frontend

```bash
streamlit run frontend/app.py
```

The UI will open at **http://localhost:8501**.

---

## 🔑 Role-Based Access

| Role | Permissions |
|------|-------------|
| **admin** | Full access to all endpoints |
| **doctor** | Create/update diagnoses; view all records |
| **receptionist** | Register patients, schedule appointments, manage billing |

---

## 📡 API Endpoints

| Module | Endpoint | Method | Description |
|--------|----------|--------|-------------|
| Auth | `/auth/register` | POST | Register a new user |
| Auth | `/auth/login` | POST | Login and get JWT token |
| Auth | `/auth/me` | GET | Get current user info |
| Patients | `/patients/` | GET / POST | List or register patients |
| Patients | `/patients/{id}` | GET / PUT / DELETE | Get, update, or delete a patient |
| Doctors | `/doctors/` | GET / POST | List or add doctors |
| Doctors | `/doctors/{id}` | GET / PUT / DELETE | Get, update, or delete a doctor |
| Appointments | `/appointments/` | GET / POST | List or schedule appointments |
| Appointments | `/appointments/{id}` | GET / PUT / DELETE | Manage a specific appointment |
| Appointments | `/appointments/patient/{id}` | GET | Get appointments for a patient |
| Diagnoses | `/diagnoses/` | GET / POST | List or add diagnoses |
| Diagnoses | `/diagnoses/{id}` | GET / PUT | Get or update a diagnosis |
| Diagnoses | `/diagnoses/patient/{id}` | GET | Get diagnoses for a patient |
| Billing | `/billing/` | GET / POST | List or create bills |
| Billing | `/billing/{id}` | GET / PUT | Get or update a bill |
| Billing | `/billing/patient/{id}` | GET | Get bills for a patient |