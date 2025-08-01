# Pharmacy Management System

## Overview

The Pharmacy Management system is a system designed to facilitate the management of pharmacy systems, such as prescriptions, purchases of medication, and patient management. It allows pharmacy staff to effectively organize, prioritize, and update their prescriptions and patients, as well as providing the ability to purchase medication ensuring a smooth and management process.

## Features

- **Prescription Management**: Input prescriptions to manage inventory, distribution, and availability of prescriptions.
- **Patient Management System**: View patients and their prescription requirements, notifications for reminders on refills, assign new prescriptions, etc.
- **Specialized Staff Accounts**: Allow pharmacy staff with specified role permissions to access their specific role features to perform their role efficiently.
- **Prescription purchasing system**: Patients are able to make purchases of prescriptions prescribed to them through an implemented point of sale system.
- **Manager Dashboard**: A specialized dashboard for managers to view higher level information, such as notificaitons for drugs, prescriptions, patients, etc.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11.7 or newer
- Django 5.0.1 or newer

### Setup and Installation

1. **Clone the Repository**

   ```shell
   git clone https://github.com/rgomez2000/Pharmacy-Management-System.git
   cd pharmacy
   ```

2. **Install the Required Packages**

   ```shell
   pip install pillow
   pip install django-currentuser
   ```
3. **Return Directory Back to Main Folder**

   ```shell
   cd ..
   ```

4. **Initialize the Database**

   ```shell
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**

   ```shell
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` in your web browser to view the application.
   
   Note: To view all of the features of the application, a superuser is available. Input **admin** as the username and **password** as the password to use the available         superuser.
