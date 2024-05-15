import streamlit as st
from database import SessionLocal
from models import Patient, Appointment, MedicalRecord
import pandas as pd
from datetime import date

def main():
    st.title("Hospital Management System")
    menu = ["Patients", "Appointments", "Medical Records"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Patients":
        manage_patients()
    elif choice == "Appointments":
        manage_appointments()
    elif choice == "Medical Records":
        manage_medical_records()

def manage_patients():
    st.subheader("Patient Management")
    session = SessionLocal()

    # Create Patient
    with st.form("Add Patient Form"):
        name = st.text_input("Name")
        dob = st.date_input("Date of Birth", max_value=date.today())
        email = st.text_input("Email")
        submit = st.form_submit_button("Submit")
        if submit:
            new_patient = Patient(name=name, dob=dob, email=email)
            session.add(new_patient)
            session.commit()
            st.success("Patient added successfully")
    
    # Read Patients
    patients = session.query(Patient).all()
    patient_df = pd.DataFrame([(p.id, p.name, p.dob, p.email) for p in patients], columns=["ID", "Name", "DOB", "Email"])
    st.table(patient_df)

    # Update Patient
    st.subheader("Update Patient")
    patient_ids = [p.id for p in patients]
    selected_id = st.selectbox("Select Patient ID to Update", patient_ids)
    selected_patient = session.query(Patient).filter(Patient.id == selected_id).first()
    if selected_patient:
        with st.form("Update Patient Form"):
            new_name = st.text_input("Name", value=selected_patient.name)
            new_dob = st.date_input("Date of Birth", value=selected_patient.dob)
            new_email = st.text_input("Email", value=selected_patient.email)
            submit = st.form_submit_button("Update")
            if submit:
                selected_patient.name = new_name
                selected_patient.dob = new_dob
                selected_patient.email = new_email
                session.commit()
                st.success("Patient updated successfully")

    # Delete Patient
    st.subheader("Delete Patient")
    delete_id = st.selectbox("Select Patient ID to Delete", patient_ids)
    if st.button("Delete"):
        patient_to_delete = session.query(Patient).filter(Patient.id == delete_id).first()
        if patient_to_delete:
            session.delete(patient_to_delete)
            session.commit()
            st.success("Patient deleted successfully")

    session.close()  # Close session after operations

def manage_appointments():
    st.subheader("Manage Appointments")
    session = SessionLocal()

    # Create Appointment
    with st.form("Add Appointment Form"):
        patient_ids = [p.id for p in session.query(Patient).all()]
        patient_id = st.selectbox("Select Patient ID", patient_ids)
        date_of_appointment = st.date_input("Date of Appointment", min_value=date.today())
        reason = st.text_input("Reason for Appointment")
        submit = st.form_submit_button("Submit")
        if submit:
            new_appointment = Appointment(patient_id=patient_id, date=date_of_appointment, reason=reason)
            session.add(new_appointment)
            session.commit()
            st.success("Appointment added successfully")
    
    # Read Appointments
    appointments = session.query(Appointment).all()
    appointment_df = pd.DataFrame([(a.id, a.patient_id, a.date, a.reason) for a in appointments], 
                                  columns=["ID", "Patient ID", "Date", "Reason"])
    st.table(appointment_df)

    # Update Appointment
    st.subheader("Update Appointment")
    appointment_ids = [a.id for a in appointments]
    selected_id = st.selectbox("Select Appointment ID to Update", appointment_ids)
    selected_appointment = session.query(Appointment).filter(Appointment.id == selected_id).first()
    if selected_appointment:
        with st.form("Update Appointment Form"):
            new_patient_id = st.selectbox("Select Patient ID", patient_ids, index=patient_ids.index(selected_appointment.patient_id))
            new_date = st.date_input("Date of Appointment", value=selected_appointment.date)
            new_reason = st.text_input("Reason for Appointment", value=selected_appointment.reason)
            submit = st.form_submit_button("Update")
            if submit:
                selected_appointment.patient_id = new_patient_id
                selected_appointment.date = new_date
                selected_appointment.reason = new_reason
                session.commit()
                st.success("Appointment updated successfully")

    # Delete Appointment
    st.subheader("Delete Appointment")
    delete_id = st.selectbox("Select Appointment ID to Delete", appointment_ids)
    if st.button("Delete"):
        appointment_to_delete = session.query(Appointment).filter(Appointment.id == delete_id).first()
        if appointment_to_delete:
            session.delete(appointment_to_delete)
            session.commit()
            st.success("Appointment deleted successfully")

    session.close()  # Close session after operations

def manage_medical_records():
    st.subheader("Manage Medical Records")
    session = SessionLocal()

    # Create Medical Record
    with st.form("Add Medical Record Form"):
        patient_ids = [p.id for p in session.query(Patient).all()]
        patient_id = st.selectbox("Select Patient ID", patient_ids)
        description = st.text_area("Description of Medical Record")
        date_of_record = st.date_input("Date of Record", max_value=date.today())
        submit = st.form_submit_button("Submit")
        if submit:
            new_record = MedicalRecord(patient_id=patient_id, description=description, date=date_of_record)
            session.add(new_record)
            session.commit()
            st.success("Medical record added successfully")
    
    # Read Medical Records
    medical_records = session.query(MedicalRecord).all()
    records_by_patient = {}
    for record in medical_records:
        if record.patient_id not in records_by_patient:
            records_by_patient[record.patient_id] = []
        records_by_patient[record.patient_id].append(record)
    
    for patient_id, records in records_by_patient.items():
        st.write(f"Patient ID: {patient_id}")
        record_df = pd.DataFrame([(r.id, r.description, r.date) for r in records], 
                                 columns=["Record ID", "Description", "Date"])
        st.table(record_df)

    # Update Medical Record
    st.subheader("Update Medical Record")
    patient_id_for_update = st.selectbox("Select Patient ID to Update Records", patient_ids)
    patient_records = session.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id_for_update).all()
    record_ids_for_update = [r.id for r in patient_records]
    if record_ids_for_update:  # Check if there are records to update
        selected_record_id = st.selectbox("Select Record ID to Update", record_ids_for_update)
        selected_record = session.query(MedicalRecord).filter(MedicalRecord.id == selected_record_id).first()
        if selected_record:
            with st.form("Update Medical Record Form"):
                new_description = st.text_area("Description of Medical Record", value=selected_record.description)
                new_date = st.date_input("Date of Record", value=selected_record.date)
                submit = st.form_submit_button("Update")
                if submit:
                    selected_record.description = new_description
                    selected_record.date = new_date
                    session.commit()
                    st.success("Medical record updated successfully")
    else:
        st.warning("No records found for the selected patient.")

    # Delete Medical Record
    st.subheader("Delete Medical Record")
    patient_id_for_delete = st.selectbox("Select Patient ID to Delete Records", patient_ids)
    patient_records = session.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id_for_delete).all()
    record_ids_for_delete = [r.id for r in patient_records]
    if record_ids_for_delete:  # Check if there are records to delete
        selected_record_id_for_delete = st.selectbox("Select Record ID to Delete", record_ids_for_delete)
        if st.button("Delete"):
            record_to_delete = session.query(MedicalRecord).filter(MedicalRecord.id == selected_record_id_for_delete).first()
            if record_to_delete:
                session.delete(record_to_delete)
                session.commit()
                st.success("Medical record deleted successfully")
    else:
        st.warning("No records found for the selected patient.")

    session.close()  # Close session after operations

if __name__ == '__main__':
    main()
