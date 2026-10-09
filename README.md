# Flask Blog Application

A modular, Object-Oriented Python web application built using Flask, SQLAlchemy, and version control best practices.

## Project Overview

This project implements a secure, modular blog platform backend. It features an Object-Oriented architecture separating HTTP routing logic from business services, database operations, and user authentication routines.

## Key Features

- **Object-Oriented Architecture:** Encapsulated business logic using dedicated service classes (`AuthService`) and data models (`User`, `Post`).
- **Defensive API Endpoint Design:** Explicit JSON payload validation, type checking, and HTTP status code handling (`400`, `401`, `422`, `500`).
- **Database Exception Safety:** Automated session rollback handling for database errors (`DataError`, `IntegrityError`, `SQLAlchemyError`) with error logging.
- **Password Security:** Password hashing and validation managed via Flask-Bcrypt.

## Project Structure

```text
flaskblog/
├── __init__.py       # Package initialization (Flask app, SQLAlchemy, Bcrypt)
├── models.py         # SQLAlchemy data models (User, Post) & OOP AuthService
├── routes.py         # HTTP endpoint controllers
├── app_errors.log    # Server application logs
run.py                # Application entry point script
README.md             # Project documentation