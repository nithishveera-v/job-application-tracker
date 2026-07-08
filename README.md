# Job Application Tracker

A full-stack Job Application Tracker built with Django and MySQL to help users organize and manage job applications efficiently. The application includes authentication, analytics dashboards, interview tracking, document uploads, and CSV export.

---

## Features

- User Registration & Login Authentication
- Add, Edit, View and Delete Job Applications (CRUD)
- Dashboard with application statistics
- Status Breakdown Chart
- Application Distribution Chart
- Interview Date Tracking
- Resume & Cover Letter Upload
- Search and Filter Applications
- Pagination (10 applications per page)
- CSV Export
- Responsive User Interface

---

## Tech Stack

### Backend
- Python
- Django

### Database
- MySQL

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

---

## Project Structure

```
jobtracker/
│── jobtracker/
│── tracker/
│── static/
│── media/
│── templates/
│── manage.py
│── requirements.txt
│── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/nithishveera-v/job-application-tracker.git
```

### Navigate into the project

```bash
cd job-application-tracker
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure MySQL

Update your database credentials inside:

```
jobtracker/settings.py
```

### Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Start the server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

## Screenshots

Add screenshots here after deploying the project.

Example:

- Login Page
- Dashboard
- Application List
- Charts
- Add Application Form

---

## Future Improvements

- Email Notifications
- Company Logo Upload
- Job Application Reminders
- Dark Mode
- Interview Notes
- Export to PDF

---

## Author

**Nithish V**

GitHub:
https://github.com/nithishveera-v

LinkedIn:
https://linkedin.com/in/nithish-veera

---

## License

This project is created for educational and portfolio purposes.