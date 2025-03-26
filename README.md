
# HeathCare-API

This is a backend system for a healthcare application built using Django, Django REST Framework (DRF), PostgreSQL, and JWT authentication. The system allows users to register, log in, and manage patient and doctor records securely. It also supports mapping patients to doctors.

## Features

* User registration and login
  
* Patient record management
  
* Doctor record management
  
* Patient-doctor mapping management
  
* RESTful API endpoints for all features

## Installation

To install the project, follow these steps:

1. Clone the repository: `git clone https://github.com/rishee10/HealthCare-API.git`
2. Navigate to the project directory: `cd HealthCare-API`
3. Install the requirements: `pip install -r requirements.txt`
4. Create a PostgreSQL database: `psql -U postgres -c "CREATE DATABASE healthcare_db;"`
5. Create a PostgreSQL user: `psql -U postgres -c "CREATE ROLE healthcare_user WITH PASSWORD 'healthcare_password';"`
6. Grant privileges to the user: `psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE healthcare_db TO healthcare_user;"`
7. Run the migrations: `python manage.py migrate`
8. Run the development server: `python manage.py runserver`

Make sure to replace the healthcare_db, healthcare_user, and healthcare_password placeholders with your actual database credentials.

   
