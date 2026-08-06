# Lakebase Support Center

An internal support ticketing system built as a Databricks App with **Lakebase** as the operational data store. Built for the Databricks AI Bootcamp — Day 1 Homework Assignment.

**App URL:** https://support-center-7474648537181325.aws.databricksapps.com

---

## Features

| Feature | Description |
|---------|-------------|
| **Dashboard** | Live stats cards showing Open / In Progress / Resolved counts |
| **Filter** | One-click filter by status on the ticket list |
| **View tickets** | Sortable table with status badges, created-by, and timestamps |
| **Create ticket** | Form with server-side validation and flash feedback |
| **Ticket detail** | Full message thread with author avatars and timestamps |
| **Add message** | Reply to any ticket with your name and message |
| **Update status** | Change Open → In Progress → Resolved from the ticket page |
| **Delete ticket** | Remove a ticket and all its messages, with a confirmation dialog |

All reads and writes go through Lakebase — no hard-coded data.

---

## Architecture

```
Databricks App (Flask + Python)
│
├── app.py          Routes and request handling
├── crud.py         SQL data access layer (psycopg3)
├── lakebase.py     Connection factory — reads URL from a static role password
├── config.py       Documents expected environment variables
│
├── Templates/
│   ├── base.html       Layout: navbar, flash messages
│   ├── index.html      Ticket list + stats dashboard
│   ├── ticket.html     Ticket detail, message thread, status update
│   └── new_ticket.html Create ticket form
│
└── static/
    └── style.css       Bootstrap 5 + custom styles
```

---

## Database Schema

**tickets**

| Column | Type | Notes |
|--------|------|-------|
| `ticket_id` | SERIAL PRIMARY KEY | Auto-incremented |
| `title` | VARCHAR(200) | Required |
| `status` | VARCHAR(20) | `open` \| `in_progress` \| `resolved` |
| `created_by` | VARCHAR(100) | Author name |
| `created_at` | TIMESTAMP | Set by the app via `NOW()` |

**ticket_messages**

| Column | Type | Notes |
|--------|------|-------|
| `message_id` | SERIAL PRIMARY KEY | Auto-incremented |
| `ticket_id` | INT REFERENCES tickets | Foreign key |
| `message_text` | TEXT | Required, max 2,000 chars |
| `author` | VARCHAR(100) | Author name |
| `created_at` | TIMESTAMP | Set by the app via `NOW()` |

---

## Environment Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `LAKEBASE_URL` | Databricks Secret (auto-injected by `app.yaml`) | Full PostgreSQL connection URL |
| `FLASK_SECRET_KEY` | Optional | Signs Flask flash messages. A random key is generated if omitted (set this in production). |

The connection URL is stored as a Databricks secret and injected by the `resources.secrets` binding in `app.yaml`. **No credentials appear in source code.**

---

## Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** (never commit this)
   ```
   LAKEBASE_URL=postgresql://student:<password>@<lakebase-host>:5432/<dbname>
   FLASK_SECRET_KEY=local-dev-key
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. Open [http://localhost:5000](http://localhost:5000)

> `python-dotenv` automatically loads `.env` when running locally.

---

## Deploying to Databricks Apps

1. **Store the Lakebase connection URL as a Databricks secret**
   ```bash
   databricks secrets put-secret database lakebase-url
   ```

2. **Deploy** from the Databricks workspace UI:
   - Navigate to **Compute → Apps → Create App**
   - Choose **Custom**, then upload or link this repository
   - `app.yaml` is read automatically — it binds the secret to `LAKEBASE_URL`

3. **Verify**
   - Open the app URL shown in the Apps UI
   - Confirm existing tickets appear on the homepage
   - Create a ticket and confirm it persists after a browser refresh

---

## Security Notes

- Credentials are stored in the Databricks secret store, not in source code
- All SQL queries use parameterized inputs — no string interpolation
- Status values are validated against an allowlist before any write
- `FLASK_SECRET_KEY` should be set via environment variable in production

---

## Lakebase Tables & Sample Records

<img width="2099" height="565" alt="image" src="https://github.com/user-attachments/assets/0a497754-f35b-49a2-9e5a-8ef3d0a70367" />

<img width="2178" height="603" alt="image" src="https://github.com/user-attachments/assets/cc9cf38c-cc6b-4ec2-bfd2-a3e8ec077666" />

---

## APP Screenshots

<img width="2061" height="761" alt="image" src="https://github.com/user-attachments/assets/d17e8050-4318-4ed1-8de9-de3136100c68" />

<img width="1984" height="717" alt="image" src="https://github.com/user-attachments/assets/c9bfe757-79af-4d58-b502-5aa14ac46373" />

<img width="2025" height="1189" alt="image" src="https://github.com/user-attachments/assets/581aad82-d7ad-4621-8594-0042039e2b0d" />

<img width="2005" height="1064" alt="image" src="https://github.com/user-attachments/assets/17875183-9442-4098-bd96-71ce109f2e3a" />

<img width="2007" height="808" alt="image" src="https://github.com/user-attachments/assets/bbe791fb-1f97-4fe7-a00d-00eb7d0cae8a" />

---












