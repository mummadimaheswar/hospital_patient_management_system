import streamlit as st
import requests
from datetime import date, datetime

# ── CONFIG ──────────────────────────────────────────────────────────
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Hospital Patient Management",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ---------- global ---------- */
    .main { background-color: #0a1628; }
    .stApp { background-color: #0a1628; color: #e0e6ed; }
    
    /* ---------- header ---------- */
    .hero-header {
        background: linear-gradient(135deg, #0b2545 0%, #13547a 50%, #00c9a7 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(0,201,167,.3);
    }
    .hero-header h1 { font-size: 2.4rem; margin: 0; }
    .hero-header p  { font-size: 1.1rem; opacity: .85; margin-top: .5rem; }

    /* ---------- stat cards ---------- */
    .stat-card {
        background: #112240;
        border-radius: 14px;
        padding: 1.4rem 1.2rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,.3);
        border-left: 5px solid;
        transition: transform .2s;
    }
    .stat-card:hover { transform: translateY(-4px); box-shadow: 0 6px 20px rgba(0,201,167,.2); }
    .stat-card h2 { margin: 0; font-size: 2rem; color: #00c9a7; }
    .stat-card p  { margin: .3rem 0 0; font-size: .9rem; color: #8892b0; }

    /* ---------- patient card ---------- */
    .patient-card {
        background: #112240;
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,.3);
        border-left: 5px solid #00c9a7;
        transition: transform .15s, box-shadow .15s;
    }
    .patient-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,201,167,.2);
    }
    .patient-card h4 { margin: 0 0 .4rem; color: #00c9a7; }
    .patient-card .info { color: #ccd6f6; font-size: .95rem; line-height: 1.7; }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: .8rem;
        font-weight: 600;
        color: white;
    }
    .badge-disease  { background: #ff6b6b; }
    .badge-id       { background: #00c9a7; }
    .badge-date     { background: #48bfe3; }

    /* ---------- sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020c1b 0%, #0b2545 100%);
        color: white;
    }
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] label { color: #ccd6f6 !important; }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover { color: #00c9a7 !important; }

    /* ---------- buttons ---------- */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        padding: .5rem 1.5rem;
        transition: all .2s;
        background-color: #00c9a7;
        color: #0a1628;
        border: none;
    }
    .stButton>button:hover {
        transform: scale(1.03);
        background-color: #00e6be;
        color: #0a1628;
    }
    
    /* ---------- form & input styling ---------- */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div,
    .stDateInput>div>div>input {
        background-color: #1a2c4e;
        color: #e0e6ed;
        border: 1px solid #233554;
    }
    .stTextInput label, .stNumberInput label,
    .stSelectbox label, .stDateInput label {
        color: #8892b0 !important;
    }
    h1, h2, h3, h4, h5, h6, .stSubheader { color: #ccd6f6 !important; }

    /* ---------- success/error ---------- */
    .op-success {
        background: #0d2818;
        border-left: 5px solid #00c9a7;
        padding: 1rem;
        border-radius: 8px;
        margin: .8rem 0;
        color: #a8e6cf;
    }
    .op-error {
        background: #2d0a0a;
        border-left: 5px solid #ff6b6b;
        padding: 1rem;
        border-radius: 8px;
        margin: .8rem 0;
        color: #ffb3b3;
    }
</style>
""", unsafe_allow_html=True)

# ── HELPERS ─────────────────────────────────────────────────────────
def api(method, path, **kwargs):
    """Small wrapper around requests that catches connection errors."""
    try:
        r = getattr(requests, method)(f"{API_URL}{path}", **kwargs)
        return r
    except requests.ConnectionError:
        st.error("⚠️ Cannot connect to the backend API. Make sure FastAPI is running on port 8000.")
        st.stop()

def fetch_patients():
    r = api("get", "/patients/")
    return r.json() if r.status_code == 200 else []

def parse_date(value):
    """Try to parse a date string in common formats, fallback to today."""
    if not value:
        return date.today()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(str(value).strip(), fmt).date()
        except ValueError:
            continue
    try:
        return date.fromisoformat(str(value).strip())
    except (ValueError, TypeError):
        return date.today()

# ── HEADER ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>🏥 Hospital Patient Management System</h1>
    <p>Manage admissions, track patients &amp; keep records — all in one place</p>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚕️ Navigation")
    page = st.radio(
        "Go to",
        ["📊 Dashboard", "➕ Add Patient", "✏️ Update Patient", "🗑️ Delete Patient", "🔍 Search Patient"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.caption("Hospital Patient Management System v2.0")
    st.caption(f"Today: {date.today().strftime('%B %d, %Y')}")

# ── PAGE: DASHBOARD ────────────────────────────────────────────────
if page == "📊 Dashboard":
    patients = fetch_patients()
    total = len(patients)

    # — stats row —
    diseases = {}
    ages = []
    for p in patients:
        diseases[p["disease"]] = diseases.get(p["disease"], 0) + 1
        ages.append(p["patient_age"])
    avg_age = round(sum(ages) / len(ages), 1) if ages else 0
    top_disease = max(diseases, key=lambda d: diseases[d]) if diseases else "N/A"

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="stat-card" style="border-color:#00c9a7;">
            <h2>{total}</h2><p>Total Patients</p>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card" style="border-color:#ff6b6b;">
            <h2>{top_disease}</h2><p>Most Common Disease</p>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="stat-card" style="border-color:#48bfe3;">
            <h2>{avg_age}</h2><p>Average Age</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("###")  # spacer

    # — patient list —
    st.subheader(f"📋 All Patients ({total})")

    if not patients:
        st.info("No patients found. Add one from the sidebar!")
    else:
        # Filters
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            search_name = st.text_input("🔎 Filter by name", key="dash_filter_name")
        with col_f2:
            all_diseases = sorted(set(p["disease"] for p in patients))
            disease_filter = st.selectbox("🦠 Filter by disease", ["All"] + all_diseases, key="dash_filter_disease")

        filtered = patients
        if search_name:
            filtered = [p for p in filtered if search_name.lower() in p["patient_name"].lower()]
        if disease_filter != "All":
            filtered = [p for p in filtered if p["disease"] == disease_filter]

        # Render cards in 2-col grid
        for i in range(0, len(filtered), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx >= len(filtered):
                    break
                p = filtered[idx]
                with col:
                    st.markdown(f"""
                    <div class="patient-card">
                        <h4>👤 {p['patient_name']}</h4>
                        <div class="info">
                            <span class="badge badge-id">ID: {p['patient_id']}</span>
                            <span class="badge badge-disease">{p['disease']}</span>
                            <span class="badge badge-date">📅 {p['admission_date']}</span>
                            <br/><br/>
                            <b>Age:</b> {p['patient_age']} years
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ── PAGE: ADD PATIENT ──────────────────────────────────────────────
elif page == "➕ Add Patient":
    st.subheader("➕ Register New Patient")
    with st.form("add_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            pid = st.number_input("Patient ID", min_value=1, step=1)
            pname = st.text_input("Patient Name")
        with c2:
            page_val = st.number_input("Age", min_value=0, max_value=150, step=1)
            pdisease = st.text_input("Disease / Diagnosis")
        pdate = st.date_input("Admission Date", value=date.today())
        submitted = st.form_submit_button("🩺 Register Patient", use_container_width=True)

    if submitted:
        if not pname or not pdisease:
            st.markdown('<div class="op-error">❌ Please fill in all fields.</div>', unsafe_allow_html=True)
        else:
            payload = {
                "patient_id": int(pid),
                "patient_name": pname,
                "patient_age": int(page_val),
                "disease": pdisease,
                "admission_date": str(pdate),
            }
            r = api("post", "/patients/", json=payload)
            if r.status_code == 200:
                st.markdown(f'<div class="op-success">✅ Patient <b>{pname}</b> registered successfully!</div>', unsafe_allow_html=True)
                st.balloons()
            else:
                detail = r.json().get("detail", "Unknown error")
                st.markdown(f'<div class="op-error">❌ {detail}</div>', unsafe_allow_html=True)

# ── PAGE: UPDATE PATIENT ───────────────────────────────────────────
elif page == "✏️ Update Patient":
    st.subheader("✏️ Update Patient Record")

    search_pid = st.number_input("Enter Patient ID to update", min_value=1, step=1, key="update_search_pid")
    if st.button("🔎 Find Patient", key="update_find_btn"):
        r = api("get", f"/patients/{int(search_pid)}")
        if r.status_code == 200:
            st.session_state["update_patient"] = r.json()
        else:
            st.session_state.pop("update_patient", None)
            st.markdown('<div class="op-error">❌ Patient not found.</div>', unsafe_allow_html=True)

    if "update_patient" in st.session_state:
        sel = st.session_state["update_patient"]
        st.markdown(f"""
        <div class="patient-card">
            <h4>👤 {sel['patient_name']}</h4>
            <div class="info">
                <span class="badge badge-id">ID: {sel['patient_id']}</span>
                <span class="badge badge-disease">{sel['disease']}</span>
                <span class="badge badge-date">📅 {sel['admission_date']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("update_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_name = st.text_input("Name", value=sel["patient_name"])
                new_age = st.number_input("Age", value=sel["patient_age"], min_value=0, max_value=150)
            with c2:
                new_disease = st.text_input("Disease", value=sel["disease"])
                new_date = st.date_input("Admission Date", value=parse_date(sel["admission_date"]))
            submitted = st.form_submit_button("💾 Save Changes", use_container_width=True)

        if submitted:
            payload = {
                "patient_name": new_name,
                "patient_age": int(new_age),
                "disease": new_disease,
                "admission_date": str(new_date),
            }
            r = api("patch", f"/patients/{sel['patient_id']}", json=payload)
            if r.status_code == 200:
                st.markdown('<div class="op-success">✅ Patient record updated successfully!</div>', unsafe_allow_html=True)
                st.session_state.pop("update_patient", None)
            else:
                detail = r.json().get("detail", "Unknown error")
                st.markdown(f'<div class="op-error">❌ {detail}</div>', unsafe_allow_html=True)

# ── PAGE: DELETE PATIENT ───────────────────────────────────────────
elif page == "🗑️ Delete Patient":
    st.subheader("🗑️ Remove Patient Record")

    search_pid = st.number_input("Enter Patient ID to delete", min_value=1, step=1, key="delete_search_pid")
    if st.button("🔎 Find Patient", key="delete_find_btn"):
        r = api("get", f"/patients/{int(search_pid)}")
        if r.status_code == 200:
            st.session_state["delete_patient"] = r.json()
        else:
            st.session_state.pop("delete_patient", None)
            st.markdown('<div class="op-error">❌ Patient not found.</div>', unsafe_allow_html=True)

    if "delete_patient" in st.session_state:
        sel = st.session_state["delete_patient"]

        st.markdown(f"""
        <div class="patient-card" style="border-left-color:#ff6b6b;">
            <h4>⚠️ You are about to delete:</h4>
            <div class="info">
                <b>ID:</b> {sel['patient_id']}<br/>
                <b>Name:</b> {sel['patient_name']}<br/>
                <b>Age:</b> {sel['patient_age']}<br/>
                <b>Disease:</b> {sel['disease']}<br/>
                <b>Admitted:</b> {sel['admission_date']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        confirm = st.checkbox("I confirm I want to delete this patient record")
        if st.button("🗑️ Delete Patient", type="primary", use_container_width=True, disabled=not confirm):
            r = api("delete", f"/patients/{sel['patient_id']}")
            if r.status_code == 200:
                st.markdown('<div class="op-success">✅ Patient deleted successfully!</div>', unsafe_allow_html=True)
                st.session_state.pop("delete_patient", None)
                st.rerun()
            else:
                detail = r.json().get("detail", "Unknown error")
                st.markdown(f'<div class="op-error">❌ {detail}</div>', unsafe_allow_html=True)

# ── PAGE: SEARCH PATIENT ──────────────────────────────────────────
elif page == "🔍 Search Patient":
    st.subheader("🔍 Search Patient by ID")

    pid = st.number_input("Enter Patient ID", min_value=1, step=1, key="search_pid")
    if st.button("🔎 Search", use_container_width=True):
        r = api("get", f"/patients/{int(pid)}")
        if r.status_code == 200:
            p = r.json()
            st.markdown(f"""
            <div class="patient-card" style="border-left-color:#2ecc71;">
                <h4>✅ Patient Found</h4>
                <div class="info">
                    <span class="badge badge-id">ID: {p['patient_id']}</span>
                    <span class="badge badge-disease">{p['disease']}</span>
                    <span class="badge badge-date">📅 {p['admission_date']}</span>
                    <br/><br/>
                    <b>Name:</b> {p['patient_name']}<br/>
                    <b>Age:</b> {p['patient_age']} years
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="op-error">❌ Patient not found.</div>', unsafe_allow_html=True)