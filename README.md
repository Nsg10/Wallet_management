# Wallet Management API

A FastAPI-based Wallet Management REST API deployed on Railway with PostgreSQL as the database.

---

## Features

- User management with create and list users
- Wallet balance update and retrieval
- Transaction history per user
- Powered by FastAPI, SQLAlchemy ORM, and PostgreSQL

---

## Setup and Run Locally

1. Clone the repository:

git clone https://github.com/Nsg10/Wallet_management.git
cd Wallet_management

text

2. Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate # Windows

text

3. Install dependencies:

pip install -r requirements.txt

text

4. Create a `.env` file at the root with your database URL:

DATABASE_URL=postgresql://<username>:<password>@localhost:<port>/<database_name>

text

5. Run the application locally:

uvicorn main:app --reload

text

6. Open API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Deployment on Railway

The project is deployed on [Railway](https://railway.app).

- PostgreSQL is provisioned via Railway plugins.
- `DATABASE_URL` environment variable is configured in Railway project settings.
- The app is served with the command:

uvicorn main:app --host 0.0.0.0 --port $PORT

text

---

## Live Demo

API is live and accessible at:

[https://web-production-81b26.up.railway.app](https://web-production-81b26.up.railway.app)

You can view and test the API endpoints at:

[https://web-production-81b26.up.railway.app/docs](https://web-production-81b26.up.railway.app/docs)

---

## Technologies Used

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Railway for deployment

---

## Author

Niharika

---

Feel free to explore the API and submit issues or contributions!
