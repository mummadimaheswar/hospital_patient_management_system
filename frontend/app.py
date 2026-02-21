import streamlit as st
import requests
from datetime import date

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Hospital Patient Management System", layout="wide")


# ── Session state helpers ──────────────────────────────────────────────────────

def get_headers():
    token = st.session_state.get("token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def api_get(path, params=None):
    try:
        r = requests.get(f"{API_BASE}{path}", headers=get_headers(), params=params, timeout=10)
        return r
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to the backend API. Make sure the FastAPI server is running on port 8000.")
        return None


def api_post(path, data=None, json=None):
    try:
        r = requests.post(f"{API_BASE}{path}", headers=get_headers(), data=data, json=json, timeout=10)
        return r
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to the backend API.")
        return None


def api_put(path, json=None):
    try:
        r = requests.put(f"{API_BASE}{path}", headers=get_headers(), json=json, timeout=10)
        return r
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to the backend API.")
        return None


def api_delete(path):
    try:
        r = requests.delete(f"{API_BASE}{path}", headers=get_headers(), timeout=10)
        return r
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to the backend API.")
        return None


# ── Authentication ─────────────────────────────────────────────────────────────

def login_page():
    st.title("🏥 Hospital Patient Management System")
    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            r = api_post("/auth/login", data={"username": username, "password": password})
            if r and r.status_code == 200:
                st.session_state["token"] = r.json()["access_token"]
                me = api_get("/auth/me")
                if me and me.status_code == 200:
                    st.session_state["user"] = me.json()
                st.success("Logged in successfully!")
                st.rerun()
            elif r:
                st.error(f"Login failed: {r.json().get('detail', 'Unknown error')}")

    st.divider()
    st.subheader("Register New User")
    with st.form("register_form"):
        reg_username = st.text_input("Username", key="reg_username")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_fullname = st.text_input("Full Name", key="reg_fullname")
        reg_role = st.selectbox("Role", ["receptionist", "doctor", "admin"], key="reg_role")
        submitted_reg = st.form_submit_button("Register")
        if submitted_reg:
            r = api_post("/auth/register", json={
                "username": reg_username,
                "password": reg_password,
                "full_name": reg_fullname,
                "role": reg_role,
            })
            if r and r.status_code == 201:
                st.success("User registered successfully! You can now log in.")
            elif r:
                st.error(f"Registration failed: {r.json().get('detail', 'Unknown error')}")


# ── Patients ───────────────────────────────────────────────────────────────────

def patients_page():
    st.header("👤 Patient Management")
    tab1, tab2, tab3 = st.tabs(["View Patients", "Register Patient", "Update / Delete"])

    with tab1:
        r = api_get("/patients/")
        if r and r.status_code == 200:
            patients = r.json()
            if patients:
                st.dataframe(patients, use_container_width=True)
            else:
                st.info("No patients registered yet.")

    with tab2:
        with st.form("add_patient"):
            c1, c2 = st.columns(2)
            first_name = c1.text_input("First Name")
            last_name = c2.text_input("Last Name")
            dob = st.date_input("Date of Birth", value=date(1990, 1, 1))
            gender = st.selectbox("Gender", ["male", "female", "other"])
            phone = st.text_input("Phone")
            email = st.text_input("Email (optional)")
            address = st.text_area("Address (optional)")
            blood_group = st.selectbox("Blood Group", ["", "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
            submitted = st.form_submit_button("Register Patient")
            if submitted:
                payload = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "date_of_birth": str(dob),
                    "gender": gender,
                    "phone": phone,
                    "email": email or None,
                    "address": address or None,
                    "blood_group": blood_group or None,
                }
                r = api_post("/patients/", json=payload)
                if r and r.status_code == 201:
                    st.success(f"Patient registered with ID {r.json()['id']}.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")

    with tab3:
        patient_id = st.number_input("Patient ID", min_value=1, step=1, key="upd_patient_id")
        with st.form("update_patient"):
            phone = st.text_input("New Phone (leave blank to skip)")
            address = st.text_area("New Address (leave blank to skip)")
            upd_submitted = st.form_submit_button("Update Patient")
            if upd_submitted:
                payload = {}
                if phone:
                    payload["phone"] = phone
                if address:
                    payload["address"] = address
                r = api_put(f"/patients/{patient_id}", json=payload)
                if r and r.status_code == 200:
                    st.success("Patient updated.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")
        if st.button("Delete Patient", key="del_patient"):
            r = api_delete(f"/patients/{patient_id}")
            if r and r.status_code == 204:
                st.success("Patient deleted.")
            elif r:
                st.error(f"Error: {r.json().get('detail', r.text)}")


# ── Doctors ────────────────────────────────────────────────────────────────────

def doctors_page():
    st.header("🩺 Doctor Management")
    tab1, tab2 = st.tabs(["View Doctors", "Add Doctor (Admin only)"])

    with tab1:
        r = api_get("/doctors/")
        if r and r.status_code == 200:
            doctors = r.json()
            if doctors:
                st.dataframe(doctors, use_container_width=True)
            else:
                st.info("No doctors registered yet.")

    with tab2:
        with st.form("add_doctor"):
            c1, c2 = st.columns(2)
            first_name = c1.text_input("First Name")
            last_name = c2.text_input("Last Name")
            specialization = st.text_input("Specialization")
            phone = st.text_input("Phone")
            email = st.text_input("Email (optional)")
            available_days = st.text_input("Available Days (e.g. Mon,Wed,Fri)")
            submitted = st.form_submit_button("Add Doctor")
            if submitted:
                payload = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "specialization": specialization,
                    "phone": phone,
                    "email": email or None,
                    "available_days": available_days or None,
                }
                r = api_post("/doctors/", json=payload)
                if r and r.status_code == 201:
                    st.success(f"Doctor added with ID {r.json()['id']}.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")


# ── Appointments ───────────────────────────────────────────────────────────────

def appointments_page():
    st.header("📅 Appointment Scheduling")
    tab1, tab2, tab3 = st.tabs(["View Appointments", "Schedule Appointment", "Update Status"])

    with tab1:
        r = api_get("/appointments/")
        if r and r.status_code == 200:
            appts = r.json()
            if appts:
                st.dataframe(appts, use_container_width=True)
            else:
                st.info("No appointments found.")

    with tab2:
        with st.form("add_appt"):
            c1, c2 = st.columns(2)
            patient_id = c1.number_input("Patient ID", min_value=1, step=1)
            doctor_id = c2.number_input("Doctor ID", min_value=1, step=1)
            appt_date = st.date_input("Appointment Date")
            appt_time = st.time_input("Appointment Time")
            reason = st.text_area("Reason (optional)")
            submitted = st.form_submit_button("Schedule Appointment")
            if submitted:
                payload = {
                    "patient_id": int(patient_id),
                    "doctor_id": int(doctor_id),
                    "appointment_date": str(appt_date),
                    "appointment_time": str(appt_time),
                    "reason": reason or None,
                    "status": "scheduled",
                }
                r = api_post("/appointments/", json=payload)
                if r and r.status_code == 201:
                    st.success(f"Appointment created with ID {r.json()['id']}.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")

    with tab3:
        with st.form("update_appt"):
            appt_id = st.number_input("Appointment ID", min_value=1, step=1)
            new_status = st.selectbox("New Status", ["scheduled", "completed", "cancelled"])
            submitted = st.form_submit_button("Update Status")
            if submitted:
                r = api_put(f"/appointments/{appt_id}", json={"status": new_status})
                if r and r.status_code == 200:
                    st.success("Appointment status updated.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")


# ── Diagnoses ──────────────────────────────────────────────────────────────────

def diagnoses_page():
    st.header("🔬 Diagnosis Management")
    tab1, tab2, tab3 = st.tabs(["View Diagnoses", "Add Diagnosis (Doctor/Admin)", "Update Diagnosis"])

    with tab1:
        r = api_get("/diagnoses/")
        if r and r.status_code == 200:
            diags = r.json()
            if diags:
                st.dataframe(diags, use_container_width=True)
            else:
                st.info("No diagnoses recorded yet.")

    with tab2:
        with st.form("add_diag"):
            c1, c2, c3 = st.columns(3)
            appointment_id = c1.number_input("Appointment ID", min_value=1, step=1)
            patient_id = c2.number_input("Patient ID", min_value=1, step=1)
            doctor_id = c3.number_input("Doctor ID", min_value=1, step=1)
            diag_date = st.date_input("Diagnosis Date")
            description = st.text_area("Diagnosis Description")
            prescription = st.text_area("Prescription (optional)")
            notes = st.text_area("Additional Notes (optional)")
            submitted = st.form_submit_button("Save Diagnosis")
            if submitted:
                payload = {
                    "appointment_id": int(appointment_id),
                    "patient_id": int(patient_id),
                    "doctor_id": int(doctor_id),
                    "diagnosis_date": str(diag_date),
                    "description": description,
                    "prescription": prescription or None,
                    "notes": notes or None,
                }
                r = api_post("/diagnoses/", json=payload)
                if r and r.status_code == 201:
                    st.success(f"Diagnosis saved with ID {r.json()['id']}.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")

    with tab3:
        with st.form("update_diag"):
            diag_id = st.number_input("Diagnosis ID", min_value=1, step=1)
            new_prescription = st.text_area("Updated Prescription (leave blank to skip)")
            new_notes = st.text_area("Updated Notes (leave blank to skip)")
            submitted = st.form_submit_button("Update Diagnosis")
            if submitted:
                payload = {}
                if new_prescription:
                    payload["prescription"] = new_prescription
                if new_notes:
                    payload["notes"] = new_notes
                r = api_put(f"/diagnoses/{diag_id}", json=payload)
                if r and r.status_code == 200:
                    st.success("Diagnosis updated.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")


# ── Billing ────────────────────────────────────────────────────────────────────

def billing_page():
    st.header("💰 Billing Management")
    tab1, tab2, tab3 = st.tabs(["View Bills", "Create Bill (Admin/Receptionist)", "Update Payment Status"])

    with tab1:
        r = api_get("/billing/")
        if r and r.status_code == 200:
            bills = r.json()
            if bills:
                st.dataframe(bills, use_container_width=True)
            else:
                st.info("No billing records found.")

    with tab2:
        with st.form("add_bill"):
            c1, c2 = st.columns(2)
            patient_id = c1.number_input("Patient ID", min_value=1, step=1)
            appointment_id = c2.number_input("Appointment ID (optional, 0 = none)", min_value=0, step=1)
            bill_date = st.date_input("Billing Date")
            description = st.text_input("Description")
            amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
            payment_status = st.selectbox("Payment Status", ["pending", "paid", "partial"])
            submitted = st.form_submit_button("Create Bill")
            if submitted:
                payload = {
                    "patient_id": int(patient_id),
                    "appointment_id": int(appointment_id) if appointment_id > 0 else None,
                    "billing_date": str(bill_date),
                    "description": description,
                    "amount": amount,
                    "payment_status": payment_status,
                }
                r = api_post("/billing/", json=payload)
                if r and r.status_code == 201:
                    st.success(f"Bill created with ID {r.json()['id']}.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")

    with tab3:
        with st.form("update_bill"):
            bill_id = st.number_input("Bill ID", min_value=1, step=1)
            new_status = st.selectbox("New Payment Status", ["pending", "paid", "partial"])
            submitted = st.form_submit_button("Update Status")
            if submitted:
                r = api_put(f"/billing/{bill_id}", json={"payment_status": new_status})
                if r and r.status_code == 200:
                    st.success("Payment status updated.")
                elif r:
                    st.error(f"Error: {r.json().get('detail', r.text)}")


# ── Main App ───────────────────────────────────────────────────────────────────

def main():
    if "token" not in st.session_state:
        login_page()
        return

    user = st.session_state.get("user", {})

    with st.sidebar:
        st.title("🏥 Hospital PMS")
        st.markdown(f"**Logged in as:** {user.get('full_name', 'Unknown')}")
        st.markdown(f"**Role:** `{user.get('role', '-')}`")
        st.divider()
        page = st.radio(
            "Navigation",
            ["Patients", "Doctors", "Appointments", "Diagnoses", "Billing"],
        )
        st.divider()
        if st.button("Logout"):
            st.session_state.clear()
            st.rerun()

    if page == "Patients":
        patients_page()
    elif page == "Doctors":
        doctors_page()
    elif page == "Appointments":
        appointments_page()
    elif page == "Diagnoses":
        diagnoses_page()
    elif page == "Billing":
        billing_page()


if __name__ == "__main__":
    main()
