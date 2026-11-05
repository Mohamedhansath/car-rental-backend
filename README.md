# Car Rental Backend — FastAPI Prototype

A Python/FastAPI backend prototype intended to support a car-rental application with user, vehicle, and booking endpoints backed by MySQL.

## Intended API areas
- User registration and login.
- Profile updates and password-reset prototype.
- Car catalogue and individual vehicle details.
- Customer booking retrieval and booking management.
- MySQL database access through mysql-connector.

## Technology
Python · FastAPI · Pydantic · MySQL · mysql-connector-python

## Current repository status
The available `main.py` currently contains its implementation as commented-out code. Treat this repository as a backend prototype/reference, not as a verified running API. It has not been represented as a live backend deployment.

## Security note
Before using this as a real service, implement secure password hashing, token-based authentication, strict CORS allow-lists, environment-based database credentials, authorization checks, input validation, and production error handling. Do not deploy the current prototype with real user data.
