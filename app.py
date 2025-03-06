from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Job, JobApplication, Payment, ExtraResource
import datetime

app = Flask(__name__)
cors = CORS(app, origins="*")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Job.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to a secure key
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change to a secure key

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)

# Base route that lists all available API endpoints with explanations
class BaseRoute(Resource):
    def get(self):
        return jsonify({
            "message": "Welcome to the Job Management API! Below are the available routes:",
            "routes": {
                "/get_jobs": "Retrieve all jobs.",
                "/get_job/<int:job_id>": "Retrieve a job by ID or job name.",
                "/get_users": "Retrieve all users.",
                "/get_user": "Retrieve a user by ID or username (e.g., /get_user?user_id=1 or /get_user?username=john_doe).",
                "/add_user": "Add a new user.",
                "/update_user/<int:user_id>": "Update a user by ID.",
                "/delete_user/<int:user_id>": "Delete a user by ID.",
                "/get_payments": "Retrieve all payments.",
                "/get_payment": "Retrieve a payment by ID or username (e.g., /get_payment?payment_id=1 or /get_payment?username=john_doe).",
                "/add_payment": "Add a new payment.",
                "/get_resources": "Retrieve all extra resources.",
                "/get_resource": "Retrieve a resource by ID, job name, or resource type (e.g., /get_resource?resource_id=1 or /get_resource?job_name=Software Engineer or /get_resource?resource_type=Document).",
                "/add_resource": "Add a new extra resource.",
                "/update_resource/<int:resource_id>": "Update a resource by ID.",
                "/delete_resource/<int:resource_id>": "Delete a resource by ID.",
                "/get_applications": "Retrieve all job applications.",
                "/get_application": "Retrieve a job application by ID, username, or job name (e.g., /get_application?application_id=1 or /get_application?username=john_doe or /get_application?job_name=Software Engineer).",
                "/add_application": "Add a new job application.",
            }
        })

# User Registration Route
class RegisterUser(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'graduate')

        if User.query.filter_by(email=email).first():
            return jsonify({"message": "User already exists"}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

# User Login Route
class LoginUser(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify(access_token=access_token), 200

# Protected Route Example
class ProtectedRoute(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200

# Job Routes
class GetJobs(Resource):
    def get(self):
        jobs = Job.query.all()  # Retrieve all jobs
        jobs_list = []
        for job in jobs:
            job_data = job.to_dict()  # Get the full job dict
            job_data.pop('applications', None)  # Remove applications field if present
            job_data.pop('extra_resources', None)  # Remove extra_resources field if present
            jobs_list.append(job_data)
        return jsonify(jobs_list)  # Return the filtered list of jobs


class GetJob(Resource):
    def get(self):
        job_id = request.args.get('job_id', type=int)
        job_name = request.args.get('job_name', type=str)

        if job_id:
            job = Job.query.get_or_404(job_id)
        elif job_name:
            job = Job.query.filter_by(title=job_name).first_or_404()
        else:
            return jsonify({"error": "Either job_id or job_name must be provided"}), 400

        job_data = job.to_dict()  # Get the full job dict
        job_data.pop('applications', None)  # Remove applications field
        job_data.pop('extra_resources', None)  # Remove extra_resources field
        return jsonify(job_data)  # Return the filtered job data

    

# User Routes
class GetUsers(Resource):
    def get(self):
        users = User.query.all()
        users_list = []
        for user in users:
            user_data = user.to_dict()
            user_data.pop('applications', None)
            user_data.pop('payments', None)
            users_list.append(user_data)
        return jsonify(users_list)

class GetUser(Resource):
    def get(self):
        user_id = request.args.get('user_id', type=int)
        username = request.args.get('username', type=str)

        if user_id:
            user = User.query.get_or_404(user_id)
        elif username:
            user = User.query.filter_by(username=username).first_or_404()
        else:
            return jsonify({"error": "Either user_id or username must be provided"}), 400

        user_data = user.to_dict()
        user_data.pop('applications', None)
        user_data.pop('payments', None)
        return jsonify(user_data)

class AddUser(Resource):
    def post(self):
        data = request.get_json()
        try:
            user = User(
                username=data['username'],
                email=data['email'],
                phone=data.get('phone'),
                password_hash=data['password_hash'],
                role=data.get('role', 'graduate')
            )
            db.session.add(user)
            db.session.commit()
            return jsonify(user.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class UpdateUser(Resource):
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        try:
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            user.phone = data.get('phone', user.phone)
            user.password_hash = data.get('password_hash', user.password_hash)
            user.role = data.get('role', user.role)

            # Update related applications
            applications = JobApplication.query.filter_by(user_id=user.id).all()
            for app in applications:
                app.user.username = user.username
                app.user.email = user.email
                app.user.phone = user.phone
                db.session.commit()

            # Update related payments
            payments = Payment.query.filter_by(user_id=user.id).all()
            for payment in payments:
                payment.user.username = user.username
                payment.user.email = user.email
                payment.user.phone = user.phone
                db.session.commit()

            db.session.commit()
            return jsonify(user.to_dict())
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class DeleteUser(Resource):
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)

        # Keep job applications and payments but retain user data in them
        applications = JobApplication.query.filter_by(user_id=user.id).all()
        for app in applications:
            app.username = user.username
            app.email = user.email
            app.phone = user.phone
            db.session.commit()

        payments = Payment.query.filter_by(user_id=user.id).all()
        for payment in payments:
            payment.username = user.username
            payment.email = user.email
            payment.phone = user.phone
            db.session.commit()

        # Delete the user, but retain the user info in applications and payments
        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted but related applications and payments retained."})

# Payment Routes
class GetPayments(Resource):
    def get(self):
        payments = Payment.query.all()
        return jsonify([payment.to_dict() for payment in payments])

class GetPayment(Resource):
    def get(self):
        payment_id = request.args.get('payment_id', type=int)
        username = request.args.get('username', type=str)

        if payment_id:
            payment = Payment.query.get_or_404(payment_id)
        elif username:
            user = User.query.filter_by(username=username).first_or_404()
            payment = Payment.query.filter_by(user_id=user.id).all()
            if not payment:
                return jsonify({"error": "No payments found for this user"}), 404
        else:
            return jsonify({"error": "Either payment_id or username must be provided"}), 400

        return jsonify([payment.to_dict() for payment in payment])

class AddPayment(Resource):
    def post(self):
        data = request.get_json()
        try:
            payment = Payment(
                user_id=data['user_id'],
                amount=5000.0,
                payment_status=data.get('payment_status', 'completed'),
                payment_date=datetime.datetime.strptime(data['payment_date'], '%Y-%m-%d %H:%M:%S')
            )
            db.session.add(payment)
            db.session.commit()

            user = User.query.get(data['user_id'])
            if payment.amount == 5000 and payment.payment_status == 'completed':
                user.role = 'premium'
                db.session.commit()

            return jsonify(payment.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

# Extra Resource Routes
class GetResources(Resource):
    def get(self):
        resources = ExtraResource.query.all()
        return jsonify([resource.to_dict() for resource in resources])

class GetResource(Resource):
    def get(self):
        resource_id = request.args.get('resource_id', type=int)
        job_name = request.args.get('job_name', type=str)
        resource_type = request.args.get('resource_type', type=str)

        if resource_id:
            resource = ExtraResource.query.get_or_404(resource_id)
        elif job_name:
            job = Job.query.filter_by(title=job_name).first_or_404()
            resource = ExtraResource.query.filter_by(job_id=job.id).all()
        elif resource_type:
            resource = ExtraResource.query.filter_by(resource_type=resource_type).all()
        else:
            return jsonify({"error": "Provide either resource_id, job_name, or resource_type."}), 400

        return jsonify([resource.to_dict() for resource in resource])

class AddResource(Resource):
    def post(self):
        data = request.get_json()

        if not data.get('job_id') or not data.get('resource_name') or not data.get('resource_type'):
            return jsonify({"error": "job_id, resource_name, and resource_type are required fields."}), 400

        try:
            job = Job.query.get(data['job_id'])
            if not job:
                job = Job(
                    title=data['job_title'],
                    location=data['job_location'],
                    salary_min=data['salary_min'],
                    salary_max=data['salary_max'],
                    job_type=data['job_type'],
                    skills_required=data['skills_required'],
                    benefits=data['benefits'],
                    application_deadline=data['application_deadline'],
                    employer=data['employer'],
                    employer_email=data['employer_email'],
                    employer_phone=data['employer_phone']
                )
                db.session.add(job)
                db.session.commit()

            resource = ExtraResource(
                job_id=job.id,
                resource_name=data['resource_name'],
                description=data.get('description', ''),
                resource_type=data['resource_type']
            )
            db.session.add(resource)
            db.session.commit()

            return jsonify(resource.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
class UpdateResource(Resource):
    def put(self, resource_id):
        resource = ExtraResource.query.get_or_404(resource_id)
        data = request.get_json()

        try:
            resource.job_id = data.get('job_id', resource.job_id)
            resource.resource_name = data.get('resource_name', resource.resource_name)
            resource.description = data.get('description', resource.description)
            resource.resource_type = data.get('resource_type', resource.resource_type)

            if 'job_id' in data:
                job = Job.query.get(data['job_id'])
                if job:
                    job.title = data.get('job_title', job.title)
                    job.location = data.get('job_location', job.location)
                    job.salary_min = data.get('salary_min', job.salary_min)
                    job.salary_max = data.get('salary_max', job.salary_max)
                    job.job_type = data.get('job_type', job.job_type)
                    job.skills_required = data.get('skills_required', job.skills_required)
                    job.benefits = data.get('benefits', job.benefits)
                    job.application_deadline = data.get('application_deadline', job.application_deadline)
                    job.employer = data.get('employer', job.employer)
                    job.employer_email = data.get('employer_email', job.employer_email)
                    job.employer_phone = data.get('employer_phone', job.employer_phone)

                    db.session.commit()

                    applications = JobApplication.query.filter_by(job_id=job.id).all()
                    for app in applications:
                        app.job.title = job.title
                        app.job.location = job.location
                        app.job.salary_min = job.salary_min
                        app.job.salary_max = job.salary_max
                        app.job.job_type = job.job_type
                        app.job.skills_required = job.skills_required
                        app.job.benefits = job.benefits
                        app.job.application_deadline = job.application_deadline
                        db.session.commit()

            db.session.commit()
            return jsonify(resource.to_dict())
        except Exception as e:
            return jsonify({"error": str(e)}), 400

class DeleteResource(Resource):
    def delete(self, resource_id):
        resource = ExtraResource.query.get_or_404(resource_id)
        job = Job.query.get_or_404(resource.job_id)

        # Get all related applications and retain job info in them
        related_applications = JobApplication.query.filter_by(job_id=job.id).all()
        for app in related_applications:
            # Keep the job details in the application, even if job is deleted
            app.job_title = job.title
            app.job_location = job.location
            app.salary_min = job.salary_min
            app.salary_max = job.salary_max
            app.job_type = job.job_type
            app.skills_required = job.skills_required
            app.benefits = job.benefits
            app.application_deadline = job.application_deadline

            db.session.commit()

        # Check if the job still has other resources; if not, delete the job
        remaining_resources = ExtraResource.query.filter_by(job_id=job.id).all()
        if not remaining_resources:
            db.session.delete(job)
        
        # Delete the resource (but not the job data from applications)
        db.session.delete(resource)
        db.session.commit()

        return jsonify({"message": "Resource deleted, but job information retained in applications."})        

# Job Application Routes
class GetApplications(Resource):
    def get(self):
        applications = JobApplication.query.all()
        return jsonify([application.to_dict() for application in applications])

class GetApplication(Resource):
    def get(self):
        application_id = request.args.get('application_id', type=int)
        username = request.args.get('username', type=str)
        job_name = request.args.get('job_name', type=str)

        if application_id:
            application = JobApplication.query.get_or_404(application_id)
        elif username:
            user = User.query.filter_by(username=username).first_or_404()
            application = JobApplication.query.filter_by(user_id=user.id).all()
            if not application:
                return jsonify({"error": "No applications found for this user"}), 404
        elif job_name:
            job = Job.query.filter_by(title=job_name).first_or_404()
            application = JobApplication.query.filter_by(job_id=job.id).all()
        else:
            return jsonify({"error": "Provide either application_id, username, or job_name."}), 400

        return jsonify([application.to_dict() for application in application])

class AddApplication(Resource):
    def post(self):
        data = request.get_json()

        try:
            application = JobApplication(
                user_id=data['user_id'],
                job_id=data['job_id'],
                status=data.get('status', 'pending'),
                cover_letter=data.get('cover_letter', ''),
                date_applied=datetime.datetime.strptime(data['date_applied'], '%Y-%m-%d %H:%M:%S')
            )
            db.session.add(application)
            db.session.commit()

            return jsonify(application.to_dict()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

# Add resources to API with specific HTTP methods and unique routes
api.add_resource(BaseRoute, '/')
api.add_resource(RegisterUser, '/register')
api.add_resource(LoginUser, '/login')
api.add_resource(ProtectedRoute, '/protected')

api.add_resource(GetJobs, '/get_jobs')
api.add_resource(GetJob, '/get_job')  # Changed this route to handle both job ID and job name
api.add_resource(GetUsers, '/get_users')
api.add_resource(GetUser, '/get_user')  # Changed this route to handle both user ID and username
api.add_resource(AddUser, '/add_user')
api.add_resource(UpdateUser, '/update_user/<int:user_id>')
api.add_resource(DeleteUser, '/delete_user/<int:user_id>')

api.add_resource(GetPayments, '/get_payments')
api.add_resource(GetPayment, '/get_payment')  # Changed this route to handle both payment ID and username
api.add_resource(AddPayment, '/add_payment')

api.add_resource(GetResources, '/get_job_resources') 
api.add_resource(GetResource, '/get_job_resource')  # Changed this route to handle ID, job name, or resource type
api.add_resource(AddResource, '/add_job_resource')
api.add_resource(UpdateResource, '/update_job_resource/<int:resource_id>')
api.add_resource(DeleteResource, '/delete_job_resource/<int:resource_id>')

api.add_resource(GetApplications, '/get_applications')
api.add_resource(GetApplication, '/get_application')  # Changed this route to handle ID, username, or job name
api.add_resource(AddApplication, '/add_application')

if __name__ == '__main__':
    app.run(debug=True)
