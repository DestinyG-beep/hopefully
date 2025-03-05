from app import app, db
from app import User, Job, JobApplication, Payment, ExtraResource
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

# Helper function to create random phone numbers in Kenyan format
def create_random_phone():
    return f"+254 {random.randint(700000000, 799999999)}"

# Seed Users with realistic info (7 users)
def seed_users():
    users = [
        User(
            username="john_doe92",
            email="john.doe92@gmail.com",
            phone=create_random_phone(),
            password_hash=generate_password_hash("password123"),
            role="graduate",  # non-premium graduate
            date_joined=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        ),
        User(
            username="jane_smith87",
            email="jane.smith87@gmail.com",
            phone=create_random_phone(),
            password_hash=generate_password_hash("securepass456"),
            role="premium_graduate",  # premium graduate
            date_joined=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        ),
        User(
            username="peter_williams",
            email="peter.williams@gmail.com",
            phone=create_random_phone(),
            password_hash=generate_password_hash("mypassword789"),
            role="graduate",  # non-premium graduate
            date_joined=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        ),
        User(
            username="mary_kenya",
            email="mary.kenya@gmail.com",
            phone=create_random_phone(),
            password_hash=generate_password_hash("adminpass321"),
            role="admin",  # admin role
            date_joined=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        ),
        User(
            username="joseph_ngugi",
            email="joseph.ngugi@gmail.com",
            phone=create_random_phone(),
            password_hash=generate_password_hash("joseph2023"),
            role="premium_graduate",  # premium graduate
            date_joined=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        ),
        User(
            username="anne_achola",
            email="anne.achola@gmail.com",
            phone=create_random_phone(),
            password_hash=generate_password_hash("securepassword"),
            role="graduate",  # non-premium graduate
            date_joined=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        ),
        User(
            username="peter_mwangi",
            email="peter.mwangi@gmail.com",
            phone=create_random_phone(),
            password_hash=generate_password_hash("securepass789"),
            role="premium_graduate",  # premium graduate
            date_joined=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        ),
    ]
    
    for user in users:
        db.session.add(user)
    db.session.commit()

# Seed Jobs with more Kenyan theme (5+ jobs)
def seed_jobs():
    jobs = [
        Job(
            title="Software Engineer",
            description="We are looking for a skilled software engineer with expertise in Python, JavaScript, and cloud technologies. Responsibilities include designing and developing software solutions, collaborating with teams, and ensuring code quality.",
            location="Nairobi, Kenya",
            salary_min=900000,  # in KES
            salary_max=1200000,  # in KES
            job_type="Full-time",
            skills_required="Python, JavaScript, Cloud Computing, Agile",
            benefits="Health insurance, Paid vacation, Retirement plan",
            application_deadline=datetime.utcnow() + timedelta(days=30),
            employer="Safaricom",
            employer_email="hr@safaricom.co.ke",
            employer_phone=create_random_phone(),
            date_posted=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        ),
        Job(
            title="Marketing Manager",
            description="We are looking for a passionate marketing manager to lead our team. Experience in digital marketing, campaign strategies, and team leadership required.",
            location="Mombasa, Kenya",
            salary_min=700000,  # in KES
            salary_max=950000,  # in KES
            job_type="Full-time",
            skills_required="Marketing Strategy, Digital Marketing, SEO, Leadership",
            benefits="Healthcare, 401(k), Paid holidays",
            application_deadline=datetime.utcnow() + timedelta(days=60),
            employer="Jumia Kenya",
            employer_email="careers@jumia.co.ke",
            employer_phone=create_random_phone(),
            date_posted=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        ),
        Job(
            title="Data Scientist",
            description="We are looking for a data scientist with expertise in machine learning, big data, and predictive analytics. You will be responsible for analyzing complex datasets and building data models.",
            location="Kisumu, Kenya",
            salary_min=1100000,  # in KES
            salary_max=1400000,  # in KES
            job_type="Full-time",
            skills_required="Python, R, SQL, Machine Learning, Data Analysis",
            benefits="Health insurance, Paid leave, Retirement plan",
            application_deadline=datetime.utcnow() + timedelta(days=45),
            employer="Kenya Data Science Ltd.",
            employer_email="jobs@kenyadatascience.co.ke",
            employer_phone=create_random_phone(),
            date_posted=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        ),
        Job(
            title="UX/UI Designer",
            description="We are looking for a UX/UI Designer to design web and mobile interfaces, collaborate with developers, and create user-friendly solutions.",
            location="Nakuru, Kenya",
            salary_min=750000,  # in KES
            salary_max=1000000,  # in KES
            job_type="Full-time",
            skills_required="Figma, Adobe XD, Wireframing, Prototyping, User Research",
            benefits="Health insurance, Paid time off, Career development opportunities",
            application_deadline=datetime.utcnow() + timedelta(days=30),
            employer="Kenya Web Solutions",
            employer_email="hr@kenyawebsolutions.co.ke",
            employer_phone=create_random_phone(),
            date_posted=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        ),
        Job(
            title="Product Manager",
            description="We are looking for a product manager to oversee product development, collaborate with various teams, and create strategic product roadmaps.",
            location="Eldoret, Kenya",
            salary_min=950000,  # in KES
            salary_max=1300000,  # in KES
            job_type="Full-time",
            skills_required="Product Strategy, Roadmapping, Agile, Communication",
            benefits="Healthcare, Stock options, Paid time off",
            application_deadline=datetime.utcnow() + timedelta(days=30),
            employer="Tech Innovation Group",
            employer_email="careers@techinnovationgroup.co.ke",
            employer_phone=create_random_phone(),
            date_posted=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        ),
    ]
    
    for job in jobs:
        db.session.add(job)
    db.session.commit()

# Seed Job Applications (Multiple applications for different users)
def seed_job_applications():
    job_applications = [
        JobApplication(
            user_id=1,  # john_doe92
            job_id=1,   # Software Engineer
            application_date=datetime.utcnow() - timedelta(days=random.randint(1, 20)),
            status="pending"
        ),
        JobApplication(
            user_id=2,  # jane_smith87 (premium graduate)
            job_id=1,   # Software Engineer
            application_date=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
            status="accepted"
        ),
        JobApplication(
            user_id=3,  # peter_williams
            job_id=3,   # Data Scientist
            application_date=datetime.utcnow() - timedelta(days=random.randint(5, 15)),
            status="pending"
        ),
        JobApplication(
            user_id=5,  # joseph_ngugi (premium graduate)
            job_id=4,   # UX/UI Designer
            application_date=datetime.utcnow() - timedelta(days=random.randint(5, 20)),
            status="pending"
        ),
        JobApplication(
            user_id=7,  # peter_mwangi (premium graduate)
            job_id=2,   # Marketing Manager
            application_date=datetime.utcnow() - timedelta(days=random.randint(3, 10)),
            status="rejected"
        )
    ]
    
    for application in job_applications:
        db.session.add(application)
    db.session.commit()

# Seed Payments for Premium Graduates only (Multiple payments)
def seed_payments():
    premium_graduates = User.query.filter_by(role="premium_graduate").all()

    for user in premium_graduates:
        payment = Payment(
            user_id=user.id,  # Only premium graduate's ID
            amount=5000.0,  # fixed amount of 5000
            payment_status="completed",
            payment_date=datetime.utcnow() - timedelta(days=random.randint(1, 20))
        )
        db.session.add(payment)
    
    db.session.commit()

# Seed Extra Resources with more detailed Kenyan insights
def seed_extra_resources():
    resources = [
        ExtraResource(
            job_id=1,  # Software Engineer
            resource_name="Mastering the Coding Interview resources",
            description="""
Industry Insights:
1. The Kenyan tech industry is rapidly growing, with companies such as Safaricom, Equity, and many startups seeking software engineers.
2. Machine learning and AI are emerging fields in Kenya, with large-scale projects being developed for mobile applications and fintech.
3. Nairobi remains a tech hub, and there is an increasing demand for engineers who understand both mobile and cloud computing.

Resume Guide:
1. Highlight proficiency in key programming languages like Python, JavaScript, and Java.
2. Showcase any personal or professional projects, especially those using machine learning or cloud computing.
3. Include any relevant certifications, such as Google Cloud or AWS certifications.

Interview Tips:
1. Be prepared to demonstrate problem-solving skills with algorithms.
2. Ensure you understand the importance of scalability in your designs.
3. Expect to explain technical concepts clearly, especially to non-technical stakeholders.
""",
            resource_type="Software Engineering resources"
        ),
        ExtraResource(
            job_id=3,  # Data Scientist
            resource_name="The Data Science Roadmap resources",
            description="""
Industry Insights:
1. Data Science is one of the fastest-growing fields in Kenya, with numerous organizations focusing on big data to improve decision-making.
2. The Nairobi tech scene is home to several data-driven companies in fintech and telecommunications.
3. Kenya's mobile-first approach has led to the development of rich datasets, perfect for machine learning and predictive analytics.

Resume Guide:
1. Highlight experience with Python, R, and SQL.
2. Include any relevant projects or Kaggle competitions you've participated in.
3. Certifications in data science or machine learning are a big plus.

Interview Tips:
1. Expect to solve complex problems using statistical methods and data manipulation.
2. Be prepared for a technical assessment using real datasets.
3. Brush up on machine learning concepts, especially classification, regression, and clustering.
""",
            resource_type="Data Science"
        ),
        ExtraResource(
            job_id=2,  # Marketing Manager
            resource_name="Digital Marketing in Kenya resources",
            description="""
Industry Insights:
1. The digital marketing landscape in Kenya is evolving, with increased focus on social media marketing and content creation.
2. Nairobi is home to many digital marketing agencies that serve international clients, creating a dynamic and competitive field.
3. Local platforms like M-KOPA and Twiga Foods are examples of digital-first companies growing through innovative marketing strategies.

Resume Guide:
1. Showcase experience in digital ad campaigns, SEO/SEM, and social media strategy.
2. Highlight any knowledge of Google Analytics, Facebook Ads, or other ad platforms.
3. Showcase leadership skills, especially if you've managed teams or projects.

Interview Tips:
1. Expect to explain your past digital campaigns and their ROI.
2. Be ready to discuss the latest trends in digital marketing in Kenya.
3. Be prepared to suggest marketing strategies for Kenyan startups and international businesses in Kenya.
""",
            resource_type="Marketing resources"
        ),
        ExtraResource(
            job_id=4,  # UX/UI Designer
            resource_name="Designing for Kenyan Audiences",
            description="""
Industry Insights:
1. UX/UI design is increasingly important in Kenya, as companies look to improve their customer experiences online.
2. There is a rise in mobile-first design due to the high smartphone penetration in Kenya.
3. Kenyan businesses are focusing on simplifying complex processes for users, especially in fintech and e-commerce platforms.

Resume Guide:
1. Highlight expertise in wireframing, prototyping, and usability testing.
2. Include a portfolio of past designs or websites, especially those focused on mobile-first designs.
3. Mention any experience designing for African or emerging market users.

Interview Tips:
1. Be ready to discuss your design process and how you conduct user research.
2. Expect to critique designs in a real-world case study.
3. Brush up on user-centered design principles and mobile UI/UX patterns.
""",
            resource_type="UX/UI Design resources"
        ),
        ExtraResource(
            job_id=5,  # Product Manager
            resource_name="Product Management in a Growing Economy",
            description="""
Industry Insights:
1. Kenya's product management field is growing, especially with tech startups in Nairobi and the rise of e-commerce platforms like Jumia.
2. Product managers need to balance user needs, business goals, and tech development, especially in the fast-paced Kenyan market.
3. Understanding the local market dynamics and consumer behavior is essential for product success in Kenya.

Resume Guide:
1. Emphasize experience with product lifecycle management from ideation to launch.
2. Highlight any leadership or cross-functional team experience.
3. Include any certifications in agile methodologies or product management tools.

Interview Tips:
1. Be ready to demonstrate your ability to prioritize features and manage product roadmaps.
2. Expect to answer scenario-based questions about launching products in Kenya or emerging markets.
3. Brush up on agile methodologies and product-market fit principles.
""",
            resource_type="Product Management resources"
        ),
        ExtraResource(
            job_id=3,  # Data Scientist
            resource_name="Big Data and Analytics in Kenya",
            description="""
Industry Insights:
1. With companies like Safaricom and Equity Bank leading the charge, Kenya is becoming a regional leader in big data and analytics.
2. Kenya's position as a mobile-first country means that data science professionals play a crucial role in mobile financial services, such as M-Pesa.
3. The demand for data scientists who can process large datasets and extract actionable insights is growing across industries.

Resume Guide:
1. Highlight experience with big data technologies like Hadoop, Spark, and data pipelines.
2. Demonstrate proficiency in data visualization tools like Tableau or Power BI.
3. Provide examples of how your analysis directly contributed to business decision-making.

Interview Tips:
1. Expect to be tested on your ability to clean and analyze large datasets.
2. Be prepared to discuss predictive analytics and its applications in mobile services.
3. Brush up on advanced statistical methods and their real-world use cases.
""",
            resource_type="Big Data & Analytics resources"
        ),
    ]
    
    for resource in resources:
        db.session.add(resource)
    db.session.commit()


# Main function to seed data
def seed_data():
    with app.app_context():
        print("Seeding data...")
        db.drop_all()  # Optional: Drop all tables before seeding (be cautious!)
        db.create_all()  # Create all tables

        seed_users()
        seed_jobs()
        seed_job_applications()
        seed_payments()  # Only premium graduates will be included
        seed_extra_resources()
        
        print("Data seeded successfully.")

# Run the seed function
if __name__ == "__main__":
    seed_data()
