# Smart Hostel Management System

A professional, clean, and highly interactive **Smart Hostel Management System** built with **Django**, **Bootstrap 5**, **HTML**, **CSS**, **JavaScript**, and **SQLite**. 

This system has been architected using Django best practices, custom database signal listeners, role-based authentication, and dynamic analytics widgets. It contains exactly two modules: the **Admin Module** and the **Student Module**, making it clean, easy to navigate, and suitable for a **BCA Final-Year Project**.

---

## 🌟 Key Features

### 1. General & Authentication
- **Role-Based Login**: Seamless authentication and redirection based on user roles (Admin vs Student).
- **Session Alerts**: Floating auto-dismissing feedback messages for all actions.
- **Premium Frontend Aesthetics**: Dark mode responsive sidebars, custom-tailored state badges (glowing indicator pills), card hover physics, and customized form focus behaviors.

### 2. Admin Module
- **Dashboard Analytics**: Dynamic stats cards and graphs (powered by Chart.js) mapping room occupancy distributions, complaints, and active leave frequencies.
- **Student Management (CRUD)**: Easily add, edit, view, and delete resident student profiles.
- **Room Allocation & Occupancy Tracker**: Registered rooms, real-time percentage progress bars of occupancy rates, capacity filters, and instant room assignments.
- **Complaint Board**: Review all complaints with filter utilities and update resolution statuses in-place.
- **Leave Request Manager**: View out-of-hostel leave applications and approve/reject them instantly with single action buttons.
- **Notice Board CRUD**: Publish, edit, and delete official hostel bulletins.

### 3. Student Module
- **Personal Dashboard**: A welcoming gradient banner with a quick profile overview, statistical count summaries, notices, and roommate logs.
- **My Profile**: View registration parameters and edit personal details like phone number and email.
- **Roommate Registry**: Track assigned room capacity and see names, courses, and phone numbers of other student roommates assigned to the same room.
- **Complaint Desk**: File maintenance or utility issues and track resolving states (Pending, In Progress, Resolved).
- **Leave Desk**: Submit out-of-hostel leave durations with validation constraints and monitor approvals.
- **Bulletin Board**: Read official notifications published by the admin.

---

## 🛠️ Tech Stack & Architecture

- **Backend**: Django 4.2.10 (MVT Architecture)
- **Database**: SQLite (default, zero-configuration)
- **Frontend**: Bootstrap 5, Vanilla CSS, FontAwesome, Chart.js
- **State Automation**: Custom Database Pre/Post-save & Post-delete signals to keep room occupied numbers and availability states perfectly accurate at the database level.

---

## ⚙️ Quick Installation & Setup

Follow these simple steps to run this application on your local machine:

### 1. Prerequisites
Ensure you have **Python (3.9+)** installed on your system.

### 2. Install Project Dependencies
Navigate to the project root directory and run:
```bash
pip install -r requirements.txt
```

### 3. Run Migrations & Setup Database
The database has already been prepared and migrations are generated. Apply them by executing:
```bash
python manage.py migrate
```

### 4. Run the Local Development Server
Start the local server with:
```bash
python manage.py runserver
```
Open your web browser and go to: `http://127.0.0.1:8000/`

---

## 🔑 Preset Credentials

To make demonstration and testing extremely easy, a default superuser account has been pre-seeded in the database:

- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Admin

*To register a new Student, log in as the Admin and click **"Add Student"** under the Student Directory.*

---

## 🗄️ Optional: Migrating from SQLite to MySQL

If your final year project presentation explicitly requires a **MySQL** server rather than **SQLite**, follow these simple steps to adapt the project database:

1. Install the Python MySQL client:
   ```bash
   pip install mysqlclient
   ```
2. Open `hostel_project/settings.py` and modify the `DATABASES` setting:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'hostel_db',
           'USER': 'your_mysql_username',
           'PASSWORD': 'your_mysql_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```
3. Open your MySQL client and create the database:
   ```sql
   CREATE DATABASE hostel_db;
   ```
4. Run Django migrations to generate the tables on MySQL and create the superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

To Run 
python manage.py runserver

to add in github