# Balkan API

Balkan API is a Django REST Framework project that serves as the backend for a real estate application. It provides a robust set of endpoints for managing properties, user accounts, and user-specific favorite listings.

## Features

* CRUD operations for property listings
* User authentication and authorization
* Management of user favorite properties


## Developer Documentation

For detailed installation instructions (including virtual environment setup), API endpoint specifications, and integration guides, please refer to our official developer documentation:

- [Developer Documentation Index](./docs/index.md)
- [API Reference](./docs/api-reference/auto-generated-docs.md)

## Getting Started (with Docker Compose)

The quickest way to get the Balkan API running for local development is using Docker Compose.

### Prerequisites

* **Docker Engine and Docker Compose**: You'll need Docker installed and running on your system, along with the Docker Compose CLI plugin.
    * **For Linux users (like Ubuntu)**: You typically install these directly via your package manager or Docker's official repositories.
    * **For macOS/Windows users**: [Docker Desktop](https://www.docker.com/products/docker-desktop) is the recommended way, as it includes both Docker Engine and Docker Compose.

### Quick Start

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:faisalakhlaq/home-api.git
    cd home-api
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file in the project root based on `.env.example` (you should have an example file). This will contain your database credentials, secret key, etc.
    ```ini
    # .env (example - adjust as per your .env.example)
    DEBUG=True
    SECRET_KEY='your_super_secret_key_for_dev'
    DATABASE_URL='postgres://user:password@db:5432/balkan_db' # Use 'db' as hostname for Docker Compose
    # ... other settings
    ```

3.  **Build and Run Services:**
    ```bash
    docker compose up --build -d
    ```

4.  **Apply Migrations:**
    ```bash
    docker compose exec backend python manage.py migrate
    ```

5.  **Create a Superuser (optional, for admin access):**
    ```bash
    docker compose exec backend python manage.py createsuperuser
    ```

6.  **Seed the Database (optional, for demo data):**
    ```bash
    docker compose exec backend make seed
    ```

The API will be available at `http://localhost:8000/`.

## Makefile Commands

For convenience, several common development tasks are available via `make` commands when running with Docker Compose:

* `make start`: Runs the backend service and drops you into its shell.
* `make run_dev`: Runs the development Gunicorn server (typically used inside the Docker container).
* `make migrate`: Applies Django database migrations.
* `make makemigrations`: Creates new Django migration files.
* `make test`: Runs backend tests.
* `make mypy`: Runs MyPy type checks.
* `make flake8`: Runs Flake8 linting.
* `make seed`: Seeds the database with demo data.

To use these, prefix them with `docker compose exec backend` (e.g., `docker compose exec backend make migrate`) or use `make start` to get into the container shell first.

## Built With

* [Django](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## License

Proprietary

## Acknowledgments
