# Sky Web App

## Overview
The **Sky Web App** is an internal health check platform built with **Django**, designed for Sky employees to assess team wellbeing through periodic voting sessions. It features role-based access, session trends, and secure authentication to facilitate structured feedback across departments.

This project was developed for the **5COSC021W Software Development** module.
Video Link: https://universityofwestminster-my.sharepoint.com/:v:/g/personal/psarroa_westminster_ac_uk/EUgI8GFmuvRHinCGMNclvR0BkgnD4WpWi4XNxohedFzAWA?e=yKeMDm&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D
---

## Features
- Secure staff **registration and login**
- Role-based access for:
  - Engineers & Team Leaders → Voting
  - Dept Leaders & Managers → Trends
  - Admins → Django Admin Panel
- Voting on **Health Cards** to assess team status
- Centralized **navigation bar** for consistent UI
- Trends dashboard with **visual graphs**
- Full **GDPR-compliant** data handling

---

## Setup Instructions (Local Development)

### 1. Clone the repository:
```bash
git clone https://github.com/your-username/Sky-Web-App.git
cd Sky-Web-App
```

### 2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install required packages:
```bash
pip install -r requirements.txt
```

### 4. Apply migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

---

## Load Fixture Data (Sample Data Setup)

Make sure the server is not running. Then, load the sample data in this order:

```bash
python3 manage.py loaddata departments.json
python3 manage.py loaddata teams.json
python3 manage.py loaddata healthcards.json
python3 manage.py loaddata users.json
python3 manage.py loaddata votes_sessions.json
```

###  Admin Access:
- **Username**: admin  
- **Email**: admin1@gmail.com  
- **Password**: admin  
- Access via: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

###  These fixtures include:
- Departments and Teams
- Pre-loaded Health Cards
- Sample users with different roles
- Example votes and sessions

---

## Technologies Used
- **Backend**: Django 5.x (Python 3)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development); PostgreSQL-ready
- **Authentication**: Django's built-in auth
- **Visualization**: Custom-styled CSS bar charts

---

## Legal & Licensing
- Compliant with **GDPR**: No identifiable vote data is stored.
- All authentication uses Django’s secure system.
- Project is **academic only**; not for commercial deployment.

---

## Team – 5SC14_15_H
- **Parham Golmohammadi**
- **Dawud Hussain**
- **Aleena Haroon**
- **A-nuur Hasan**
- **Hasan Jaafar**
