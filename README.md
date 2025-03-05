# Job Portal System

## Overview

This is a job portal system that enables different types of users (Normal Graduates, Premium Graduates, and Admins) to manage job applications, access job resources, and perform other actions based on their roles.

### Features
- **Normal Graduates**: Can search for jobs, apply, and manage their account.
- **Premium Graduates**: Can access additional job resources and apply for jobs.
- **Admins**: Have full control over users, job applications, resources, and payments.

---

## Table of Contents
- [Overview](#overview)
- [Roles and Permissions](#roles-and-permissions)
- [API Endpoints](#api-endpoints)
- [JSON Examples](#json-examples)


---

## Roles and Permissions

### Everyone
#in the site everyone can update or delete their accounts:
  - `/add_user`  #log in
  - `/update_user`
  - `/delete_user`

### Normal Graduate
- **Can**: 
  - Search for jobs
  - Apply for jobs
  - Update or delete their account
- **Endpoints**:
  - `/get_jobs`
   - `/get_job`  #search function
  - `/add_application`

### Premium Graduate and Admin
- **Can**: 
 - Search for jobs
  - Access all the features of Normal Graduates
  - Access job resources
  - Apply for jobs
- **Endpoints**:
  - `/get_job_resources`
 - `/get_job_resource` #search function
  - `/add_application`

### Admin
- **Can**: 
  - Full control over all users, applications, payments, and job resources
- **Endpoints**:
  - `/get_users`
  - `/get_user` #search function
  - `/get_applications`
  - `/get_application` #search function
  - `/get_payments`
   - `/get_payment` #search function  
  - `/add_job_resource`
  - `/update_job_resource`
  - `/delete_job_resource`

---

### Admin Features
- **`/get_users`**: View and manage all users.
- **`/get_applications`**: View job applications.
- **`/get_payments`**: View payment history.
- **`/add_job_resource`**: Add new job resources.
- **`/update_job_resource`**: Update existing job resources.
- **`/delete_job_resource`**: Delete job resources.

---

### 1. Jobs for Graduates
```json
{
  "get_jobs": [
    {
      "title": "Software Developer",
      "location": "New York, NY",
      "salary_min": 60000,
      "salary_max": 100000,
      "job_type": "Full-time",
      "skills_required": "Python, JavaScript",
      "benefits": "Health insurance, Paid time off",
      "application_deadline": "2025-05-01",
      "employer": "Tech Corp"
    },
    {
      "title": "Data Analyst",
      "location": "Remote",
      "salary_min": 50000,
      "salary_max": 85000,
      "job_type": "Part-time",
      "skills_required": "SQL, Excel, Python",
      "benefits": "Flexible hours",
      "application_deadline": "2025-04-15",
      "employer": "Data Solutions"
    }
  ]
}
