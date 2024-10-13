# Financial Records Entry System

This application allows you to track your financial transactions (credits and debits) on a single account and view the running total.

## Overview

This application consists of:

- **Front End**: A Single Page Application (SPA) built with TypeScript.
- **Backend**: A Flask-based server.
- **Database**: PostgreSQL.
- **Containerization**: Dockerized for easy deployment.

### Features

#### Front End Application

- Displays the current account balance.
- Lists all recorded transactions.
- Allows you to add new transactions.
- Enables modification of existing transactions.
- Styled with CSS for a clean user interface.

#### Backend Application

- **API Endpoints**:
  - Create transactions
  - Retrieve all transactions
  - Retrieve a specific transaction
  - Modify a transaction
  - Remove a transaction
- Validates all received payloads to ensure data integrity.
- Includes Swagger UI for API documentation.

#### Database

- Utilizes PostgreSQL.
- SQLAlchemy Object Relational Mapper.
- Migrations with Flask-Migrate.

### Extras

- Automated tests.
- Error handling

## Getting Started

   ```bash
  > git clone [repository-url]
  > cd tyme-bank-transactions
  > docker compose up --build
    (In a separate terminal window once previous command is completed) 
  > docker compose -f docker-compose.migrate.yml run --rm -e MESSAGE="Initial Migration" migrate
   ```
   - Navigate to http://localhost:5000 for UI, and http://localhost:5000/apidocs for swagger docs. 
