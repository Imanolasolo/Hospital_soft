from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    date = Column(Date, nullable=False)
    reason = Column(String, nullable=False)
    patient = relationship('Patient', back_populates='appointments')

class MedicalRecord(Base):
    __tablename__ = 'medical_records'
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    patient = relationship('Patient', back_populates='medical_records')

Patient.appointments = relationship('Appointment', order_by=Appointment.id, back_populates='patient')
Patient.medical_records = relationship('MedicalRecord', order_by=MedicalRecord.id, back_populates='patient')

def init_db():
    engine = create_engine('sqlite:///hospital.db')
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)

Session = init_db()
