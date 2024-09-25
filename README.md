# PBMS

## Overview

The Pharmacy Management system is a system designed to facilitate the management of pharmacy systems, such as prescriptions, purchases of medication, and patient management. It allows pharmacy staff to effectively organize, prioritize, and update their prescriptions and patients, as well as providing the ability to purchase medication ensuring a smooth and management process.

## Features

- **Prescription Management**: Input prescriptions to manage inventory, distribution, and availability of prescriptions.
- **Patient Management System**: View patients and their prescription requirements, notifications for reminders on refills, assign new prescriptions, etc.
- **Patient and Staff Accounts**: Allow patients to make accounts to view their indivudal prescriptions and information.
- **Prescription purchasing system**: Patients are able to make purchases of prescriptions prescribed to them.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.11.7
- Django 5.0.1

### Setup and Installation

1. **Clone the Repository**

   ```shell
   git clone https://github.com/qzydustin/Product-Backlog-Management-System.git
   cd pharmacy
   ```

2. **Initialize the Database**

   ```shell
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Run the Development Server**

   ```shell
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` in your web browser to view the application.
