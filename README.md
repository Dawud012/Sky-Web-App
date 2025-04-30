How to Set Up Sky Health Check – Fixture Load Guide

Make sure migrations are applied:


python3 manage.py makemigrations
python3 manage.py migrate
Load fixtures in order:


python3 manage.py loaddata departments.json
python3 manage.py loaddata teams.json
python3 manage.py loaddata healthcards.json
python3 manage.py loaddata users.json
python3 manage.py loaddata votes_sessions.json

Admin login details:
Username: admin
Email: admin1@gmail.com
Password: admin

Login at: http://127.0.0.1:8000/admin

Notes:
These fixtures will populate the system with:
Departments
Teams
Voting cards

Example users (Engineers, Team Leaders, Managers)

Voting sessions and submissions
