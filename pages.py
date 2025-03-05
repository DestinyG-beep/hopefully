#Evryone can log into this site
#/add_user 
#and based on their role they will have acess to certain functions and pages


#SITE AND PAGES:

#in the site everyone can update or delete their accounts:
#/update users
#/delete users

{
#Normal graduates
#They can apply pay for premium and ssearch for jobs 
#/add_application
#/add payment

# This page will be for normal graduates after they log in:
      "get_jobs": [
    {
      "title": "Software Developer",
      "description": "Develop web applications.",
      "location": "New York, NY",
      "salary_min": 60000,
      "salary_max": 100000,
      "job_type": "Full-time",
      "skills_required": "Python, JavaScript",
      "benefits": "Health insurance, Paid time off",
      "application_deadline": "2025-05-01 00:00:00",
      "employer": "Tech Corp",
      "employer_email": "hr@techcorp.com",
      "employer_phone": "+1 555-555-5555"
    },
    {
      "title": "Data Analyst",
      "description": "Analyze large datasets.",
      "location": "Remote",
      "salary_min": 50000,
      "salary_max": 85000,
      "job_type": "Part-time",
      "skills_required": "SQL, Excel, Python",
      "benefits": "Flexible hours",
      "application_deadline": "2025-04-15 00:00:00",
      "employer": "Data Solutions",
      "employer_email": "careers@datasolutions.com",
      "employer_phone": "+1 555-123-4567"
    }


  ],
#premium graduates and admin:
#They can search for jobs
#premium graduate:
#/add_application

#admin:
#/add_application
#/add_job resource
#/update_job_resource
#/delete_job resource

   # This page will be for normal graduates after they log in:
  "get_job_resources": [
    {
      "title": "Software Developer",
      "description": "Develop web applications.",
      "location": "New York, NY",
      "salary_min": 60000,
      "salary_max": 100000,
      "job_type": "Full-time",
      "skills_required": "Python, JavaScript",
      "benefits": "Health insurance, Paid time off",
      "application_deadline": "2025-05-01 00:00:00",
      "employer": "Tech Corp",
      "employer_email": "hr@techcorp.com",
      "employer_phone": "+1 555-555-5555",
      "resources": [
        {
          "id": 1,
          "resource_name": "Job Interview Tips",
          "description": "A guide to acing your job interview.",
          "resource_type": "PDF"
        }
      ]
    },
    {
      "title": "Data Analyst",
      "description": "Analyze large datasets.",
      "location": "Remote",
      "salary_min": 50000,
      "salary_max": 85000,
      "job_type": "Part-time",
      "skills_required": "SQL, Excel, Python",
      "benefits": "Flexible hours",
      "application_deadline": "2025-04-15 00:00:00",
      "employer": "Data Solutions",
      "employer_email": "careers@datasolutions.com",
      "employer_phone": "+1 555-123-4567",
      "resources": [
        {
          "id": 2,
          "resource_name": "Salary Negotiation Tips",
          "description": "How to negotiate your salary effectively.",
          "resource_type": "Article"
        }
      ]
    }
  ],

 #These extra pages will be for admin:
#This page will be for users access by admins :
#They can search for specific users too

  "get_users":[
  {
    "username": "john_doe",
    "email": "john.doe@example.com",
    "phone": "123-456-7890",
    "role": "graduate",
    "date_joined": "2025-03-05T00:00:00",

  },
  {
    "username": "jane_smith",
    "email": "jane.smith@example.com",
    "phone": "987-654-3210",
    "role": "premium",
    "date_joined": "2025-03-05T00:00:00",

  }
],

#This page will be for applications acces by admins :
#where they veiw all aplications
#They can search

  "get_applications": [
  {
    "application_date": "2025-03-05T14:20:00",
    "status": "pending",
    "user": {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "phone": "123-456-7890",
        "role": "graduate",
        "date_joined": "2023-06-10T09:30:00"
    },
    "job": {
        "title": "Software Developer",
        "description": "Develop and maintain software applications.",
        "location": "New York, NY",
        "salary_min": 60000.00,
        "salary_max": 90000.00,
        "job_type": "Full-time",
        "skills_required": "Python, JavaScript, SQL",
        "benefits": "Health insurance, 401(k), Paid time off",
        "application_deadline": "2025-04-01T23:59:59",
        "employer": "TechCorp Inc.",
        "employer_email": "contact@techcorp.com",
        "employer_phone": "987-654-3210",
        "date_posted": "2025-03-01T12:00:00",
        "is_active": "true"
    }
}

  ],


#This page will be for payment acces by admins :
#where they veiw all payments
#They can search

  "get_payments": [
    {
      "amount": 5000.0,
      "payment_status": "completed",
      "payment_date": "2025-03-01 12:00:00",
      "user": {
        "username": "john_doe",
        "email": "john@example.com"
      }
    },
    {
      
      "amount": 5000.0,
      "payment_status": "completed",
      "payment_date": "2025-02-20 14:30:00",
      "user": {
        "username": "jane_doe",
        "email": "jane@example.com"
      }
    }
  ]
}
