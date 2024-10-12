Financial Records Entry System 

This application allows you to track your financial transactions (credits and debits) on a single account and view the running total.

Overview

- A Front End SPA powered by Typescript
- A Flask backend 
- A postgres database
- Dockerized

1. Front end application

- Displays an account balance
- Lists recorded transactions
- Adds a new transaction
- Modifiable transactions
- CSS

2. Backend application

- Endpoints to create transactions, retrieve all transactions, retreive an individual transaction, modify a transaction and remove a transaction
- Validates all receives payloads
- Swagger UI available

3. Database

- PostgreSQL database
- SQLAlchemy ORM
- Flask-Migrate for migrations

4. Extras

- Automated tests
- Error handling

Getting started

clone this repository
cd tymebankapp
docker compose up --build
navigate to localhost:5000 for main application
navigate to localhost:5000/apidocs for swagger documentation

