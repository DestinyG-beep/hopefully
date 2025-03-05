from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, event
from sqlalchemy.orm import validates, relationship
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import re

# Initialize the SQLAlchemy object
db = SQLAlchemy(metadata=MetaData())



# Base User class for common attributes
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="graduate")
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    payments = db.relationship('Payment', back_populates='user', lazy=True, overlaps="user_payment")
    applications = db.relationship('JobApplication', back_populates='user', lazy=True, overlaps="user_application")

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address.")
        return email

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long.")
        return username

    def to_dict(self):
        user_dict = {
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "date_joined": self.date_joined,
            "payments": [payment.to_dict() for payment in self.payments],
            "applications": [app.to_dict() for app in self.applications]
        }
        return user_dict

# Job model with employer contact information
class Job(db.Model, SerializerMixin):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary_min = db.Column(db.Float, nullable=True)
    salary_max = db.Column(db.Float, nullable=True)
    job_type = db.Column(db.String(50), nullable=False)
    skills_required = db.Column(db.String(255), nullable=True)
    benefits = db.Column(db.Text, nullable=True)
    application_deadline = db.Column(db.DateTime, nullable=False)
    employer = db.Column(db.String(100), nullable=False)
    employer_email = db.Column(db.String(120), nullable=False)
    employer_phone = db.Column(db.String(20), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    applications = db.relationship('JobApplication', back_populates='job', lazy=True)
    extra_resources = db.relationship('ExtraResource', back_populates='job', lazy=True)

    @validates('salary_min', 'salary_max')
    def validate_salary(self, key, salary):
        if salary is not None and salary < 0:
            raise ValueError("Salary must be a positive number.")
        return salary

    @validates('application_deadline')
    def validate_application_deadline(self, key, application_deadline):
        if application_deadline < datetime.utcnow():
            raise ValueError("Application deadline must be in the future.")
        return application_deadline

    @validates('job_type')
    def validate_job_type(self, key, job_type):
        valid_job_types = ['Full-time', 'Part-time', 'Contract', 'Internship', 'Temporary']
        if job_type not in valid_job_types:
            raise ValueError(f"Invalid job type. Allowed types: {', '.join(valid_job_types)}.")
        return job_type

    def to_dict(self):
        job_dict = {
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "salary_min": self.salary_min,
            "salary_max": self.salary_max,
            "job_type": self.job_type,
            "skills_required": self.skills_required,
            "benefits": self.benefits,
            "application_deadline": self.application_deadline,
            "employer": self.employer,
            "employer_email": self.employer_email,
            "employer_phone": self.employer_phone,
            "date_posted": self.date_posted,
            "is_active": self.is_active,
            "applications": [application.to_dict() for application in self.applications],
            "extra_resources": [resource.to_dict() for resource in self.extra_resources]
        }
        return job_dict

# JobApplication model
class JobApplication(db.Model, SerializerMixin):
    __tablename__ = 'job_applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pending")

    user = db.relationship('User', back_populates='applications', lazy=True)
    job = db.relationship('Job', back_populates='applications', lazy=True)

    @validates('status')
    def validate_status(self, key, status):
        if status not in ["pending", "accepted", "rejected"]:
            raise ValueError("Invalid application status.")
        return status

    def to_dict(self):
        app_dict = {
            "application_date": self.application_date,
            "status": self.status,
            "user": {
                "username": self.user.username,
                "email": self.user.email,
                "phone": self.user.phone,
                "role": self.user.role,
                "date_joined": self.user.date_joined
            },
            "job": {
                "title": self.job.title,
                "description": self.job.description,
                "location": self.job.location,
                "salary_min": self.job.salary_min,
                "salary_max": self.job.salary_max,
                "job_type": self.job.job_type,
                "skills_required": self.job.skills_required,
                "benefits": self.job.benefits,
                "application_deadline": self.job.application_deadline,
                "employer": self.job.employer,
                "employer_email": self.job.employer_email,
                "employer_phone": self.job.employer_phone,
                "date_posted": self.job.date_posted,
                "is_active": self.job.is_active
            }
        }
        return app_dict

# Payment model with fixed 5000 amount
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False, default=5000)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.String(50), default="completed")

    user = db.relationship('User', back_populates='payments', lazy=True)

    @validates('amount')
    def validate_amount(self, key, amount):
        # Ensure the amount is always 5000
        if amount != 5000:
            raise ValueError("Payment amount must always be 5000.")
        return amount

    def to_dict(self):
        payment_dict = {
            "amount": self.amount,
            "payment_date": self.payment_date,
            "payment_status": self.payment_status,
            "user": {
                "username": self.user.username,
                "email": self.user.email,
                "phone": self.user.phone,
                "role": self.user.role,
                "date_joined": self.user.date_joined
            }
        }
        return payment_dict

# ExtraResource model
class ExtraResource(db.Model, SerializerMixin):
    __tablename__ = 'extra_resources'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    resource_name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    resource_type = db.Column(db.String(50), nullable=False)

    job = db.relationship('Job', back_populates='extra_resources')

    def to_dict(self):
        resource_dict = {
            "resource_name": self.resource_name,
            "description": self.description,
            "resource_type": self.resource_type,
            "job": {
                "title": self.job.title,
                "description": self.job.description,
                "location": self.job.location,
                "salary_min": self.job.salary_min,
                "salary_max": self.job.salary_max,
                "job_type": self.job.job_type,
                "skills_required": self.job.skills_required,
                "benefits": self.job.benefits,
                "application_deadline": self.job.application_deadline,
                "employer": self.job.employer,
                "employer_email": self.job.employer_email,
                "employer_phone": self.job.employer_phone,
                "date_posted": self.job.date_posted,
                "is_active": self.job.is_active
            }
        }
        return resource_dict
