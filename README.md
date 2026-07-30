# HelpCore

**An internal IT support ticketing API built with Django & Django REST Framework.**

---

## Why This Exists

During an internship, I was responsible for onboarding staff onto an existing internal IT support tool. Two problems stood out immediately:

1. **One generic dashboard for everyone** — employees and administrators saw the exact same view, with nothing tailored to what each person actually needed to do.
2. **Slow load times** — the tool took so long to open that staff began avoiding it entirely, choosing instead to walk to the IT office or send informal emails rather than file a proper ticket.

When this was raised, the response was essentially to accept email as an acceptable fallback — suggesting IT staff themselves weren't fully engaged with the tool either. The result was a support process with no reliable record, no clear ownership, and no accountability when requests went unacknowledged.

**HelpCore is built to directly address this**: fast, role-specific access, and a system that actively surfaces ignored requests instead of silently losing them.

---

## Features

- **Custom authentication** — login via `employee_id` (not username), with auto-generated unique IDs
- **Two-factor login (2FA)** — password check, followed by a 5-digit one-time code emailed to the user
- **Email verification** — new accounts must verify their email via a time-limited link before logging in
- **Role-based access** — Employees, IT Staff, and Admins each see only what's relevant to them, through the same API endpoints
- **Automatic ticket routing** — new tickets are automatically assigned to the correct IT staff member based on category
- **Guarded status lifecycle** — IT staff can move a ticket forward, but only the employee who filed it can close or reopen it
- **Threaded comments & file attachments** — full conversation history per ticket, with type/size-restricted uploads
- **Ticket history filtering** — employees can view past tickets by status
- **Escalation checks** — a management command (and Admin-only endpoint) flags tickets that have gone too long without being accepted
- **JWT authentication** — secure, token-based API access
- **Paginated, documented API** — every endpoint tested and documented via Postman

---

## Tech Stack

- **Backend:** Django 6.0, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** Custom User model, JWT (`djangorestframework-simplejwt`), 2FA via email OTP
- **Email:** Gmail SMTP (`python-decouple` for secrets management)
- **Other libraries:** `drf-nested-routers`, `psycopg2-binary`

---

## API Documentation

Full endpoint documentation, with example requests and responses, is published here:

**[HelpCore API Documentation](https://documenter.getpostman.com/view/44807174/2sBY4SNej9)**

A Postman collection is also included in this repo at `postman/HelpCore API.postman_collection.json`.

---

## Authentication Flow

HelpCore uses two-factor authentication rather than a single-step login:

1. **`POST /api/register/`** *(Admin only)* — creates a new user and sends a welcome email with a verification link
2. **`GET /api/verify-email/{token}/`** — activates the account (link expires after 2 hours)
3. **`POST /api/login/`** — checks `employee_id` + password, then emails a 5-digit one-time code
4. **`POST /api/verify-otp/`** — checks the code and returns `access` + `refresh` JWT tokens
5. Include the `access` token as a **Bearer Token** on all subsequent requests
6. **`POST /api/token/refresh/`** — exchanges the `refresh` token for a new `access` token once it expires

---

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL (running locally)
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) for sending email

### Setup

```bash
# Clone the repository
git clone https://github.com/Quincythx/HelpCore.git
cd HelpCore

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the project root:
DB_NAME=helpcore_db
DB_USER=postgres
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_character_app_password

Create the PostgreSQL database (via `psql` or pgAdmin):

```sql
CREATE DATABASE helpcore_db;
```

Run migrations and create your first Admin account:

```bash
python manage.py migrate
python manage.py createsuperuser
```

Start the server:

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`, with the Django admin panel at `http://127.0.0.1:8000/admin/`.

### Checking for Overdue Tickets

Run this manually, or schedule it (e.g. via Task Scheduler / cron) to run periodically:

```bash
python manage.py check_overdue_tickets
```

---

## Project Structure
HelpCore/
├── accounts/ # Custom User model, registration, email verification, 2FA login
├── tickets/ # Category, Ticket, Comment, Attachment models, views, permissions
│ └── management/
│ └── commands/ # check_overdue_tickets management command
├── helpCore/ # Project settings, URL routing
├── postman/ # Exported Postman collection
└── media/ # Uploaded ticket attachments (local dev only, gitignored)

---

## Design Decisions & Known Simplifications

A few deliberate simplifications were made for this phase, documented here rather than hidden:

- **Auto-assignment is one-to-one** — each ticket category maps to exactly one IT staff member, with no load-balancing across multiple staff or handling of unavailability.
- **Escalation checks are on-demand**, not a continuously running background process. The underlying logic (identifying overdue tickets) is complete and correct; it currently runs via a management command rather than a scheduler like Celery.
- **File attachments are stored locally**, not in cloud object storage (e.g. AWS S3). This is appropriate for development but would need to change for a production deployment, since local storage doesn't scale across multiple servers and isn't durable against server rebuilds.
- **Employee ID generation** uses a simple incrementing scheme based on the last created user. This is reliable under normal use but isn't fully safe against very high concurrent signups — a production system would use a database-level sequence instead.

---

## Roadmap

**Phase 2 (planned)**
- Fully automated, real-time escalation via Celery + a task scheduler
- Full status-change audit trail (who changed what, and when)
- Automated reminder emails on a timer

**Phase 3 (planned)**
- Admin analytics dashboard (ticket volume, resolution times, recurring issues)
- Weekly/monthly reporting

---

## Author

Built by [Quincy](https://github.com/Quincythx) as a project in Django & Django REST Framework.