# Installation & Setup

This guide provides instructions on how to set up the Balkan API development environment on your local machine. You can choose between using Docker Compose (recommended) or a Python virtual environment.

---

## Table of Contents

1.  [Prerequisites](#1-prerequisites)
    * [For Docker Compose Setup](#for-docker-compose-setup)
    * [For Virtual Environment Setup](#for-virtual-environment-setup)
2.  [Get the Code](#2-get-the-code)
3.  [Configure Environment Variables](#3-configure-environment-variables)
4.  [Choose Your Setup Method](#4-choose-your-setup-method)
    * [Option A: Setup with Docker Compose (Recommended)](#option-a-setup-with-docker-compose-recommended)
    * [Option B: Setup with Python Virtual Environment](#option-b-setup-with-python-virtual-environment)
5.  [Next Steps](#5-next-steps)

---

## 1. Prerequisites

Before you begin, ensure you have the following installed:

### For Docker Compose Setup:

* **Docker Engine**: The core Docker daemon that runs containers.
* **Docker Compose CLI plugin (V2)**: The command-line tool for defining and running multi-container Docker applications (the `docker compose` command, not `docker-compose`).

    * **How to install on Linux (e.g., Ubuntu):** You typically install Docker Engine and the Docker Compose plugin directly via your system's package manager or Docker's official installation instructions for your distribution. Example for Ubuntu:
        ```bash
        sudo apt update
        sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        sudo usermod -aG docker $USER # Add your user to the docker group to run without sudo (requires re-login)
        ```
        Refer to the [official Docker documentation for your specific Linux distribution](https://docs.docker.com/engine/install/) for the most up-to-date and complete instructions.
    * **For macOS/Windows users**: [Docker Desktop](https://www.docker.com/products/docker-desktop) is the recommended way to get Docker Engine and Docker Compose, as it provides a convenient GUI and manages the underlying virtualization.

### For Virtual Environment Setup:

* **Python 3.x**: Recommended Python version (e.g., Python 3.10+).
* **pip**: Python package installer (usually comes with Python).
* **[Virtualenv](https://virtualenv.pypa.io/en/latest/)**: A tool to create isolated Python environments (`pip install virtualenv`).
* **Database**:
    * **PostgreSQL**: (Recommended for production parity). You'll need to install and run a PostgreSQL server locally.

---

## 2. Get the Code

First, clone the repository to your local machine:

```bash
git clone git@github.com:faisalakhlaq/home-api.git
cd home-api
```

---

## 3. Configure Environment Variables

The Balkan API uses environment variables for sensitive information and configuration.

1.  **Create a `.env` file** in the project's root directory.
2.  **Copy the contents from `.env.example`** (which should be provided in your repository) into your new `.env` file.
3.  **Adjust the values** in your `.env` file based on your specific setup (Docker Compose or Virtual Environment).

---

## 4. Choose Your Setup Method

### Option A: Setup with Docker Compose (Recommended)

This method packages the application and its dependencies into Docker containers, providing a consistent and isolated development environment.

1.  **Build the Docker images:**
    This command builds the `backend` service image as defined in your `docker-compose.yml`.
    ```bash
    docker compose build backend
    ```

2.  **Start the services:**
    This command starts all services defined in `docker-compose.yml` (e.g., `backend`, `db`). The `-d` flag runs them in detached mode (in the background).
    ```bash
    docker compose up -d
    ```
    *To view logs: `docker compose logs -f`*
    *To stop services: `docker compose down`*

3.  **Run Database Migrations:**
    Once the `backend` service is running, apply the database schema migrations.
    ```bash
    docker compose exec backend python manage.py migrate
    ```

4.  **Create a Superuser (Optional):**
    For accessing the Django admin panel.
    ```bash
    docker compose exec backend python manage.py createsuperuser
    ```

5.  **Seed the Database (Optional):**
    Populate your database with initial data for development and testing. This uses the `make seed` command defined in your Makefile.
    ```bash
    docker compose exec backend make seed
    ```

6.  **Access the API:**
    The Balkan API should now be running and accessible at `http://localhost:8000/`.

#### Useful Docker Compose Commands:

* **Start services (build if needed):**
    ```bash
    docker compose up
    ```
* **Build images and start services in detached mode:**
    ```bash
    docker compose up --build -d
    ```
* **Stop and remove containers, networks, and volumes:**
    ```bash
    docker compose down
    ```
* **Restart just the backend service:**
    ```bash
    docker compose restart backend
    ```
* **Follow logs for the backend service:**
    ```bash
    docker compose logs -f backend
    ```
* **Get a shell inside the running backend container:**
    ```bash
    docker compose exec backend bash
    ```
    *From here, you can run `python manage.py ...` or `make ...` commands directly.*

### Option B: Setup with Python Virtual Environment

This method uses a local Python installation and `virtualenv` to create an isolated environment for your project dependencies.

1.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to avoid conflicts with other Python projects.
    ```bash
    python -m venv env
    source env/bin/activate # On Linux/macOS
    # For Windows (PowerShell): .\env\Scripts\Activate.ps1
    # For Windows (Cmd): .\env\Scripts\activate.bat
    ```
    *You'll see `(env)` prefixed to your terminal prompt, indicating the virtual environment is active.*

2.  **Install Python Dependencies:**
    Install all required Python packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Database:**
    Ensure your `DATABASE_URL` in the `.env` file is configured correctly for your local database (e.g., PostgreSQL or SQLite).
    * **For PostgreSQL**: Make sure your local PostgreSQL server is running and you've created a database and user as specified in your `DATABASE_URL`.

4.  **Run Database Migrations:**
    Apply the database schema migrations.
    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (Optional):**
    For accessing the Django admin panel.
    ```bash
    python manage.py createsuperuser
    ```

6.  **Seed the Database (Optional):**
    Populate your database with initial data for development and testing.
    ```bash
    # Ensure your virtual environment is active
    make seed
    ```

7.  **Run the Development Server:**
    Start the Django development server.
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

8.  **Deactivate Virtual Environment:**
    When you're done working, you can exit the virtual environment:
    ```bash
    deactivate
    ```

---

## 5. Next Steps

Now that your API is up and running, you can:

* **Explore API Endpoints**: Check out the [API Reference](../api-reference/properties.md) to understand the available endpoints.
* **Test with Postman/Insomnia**: Use tools like Postman or Insomnia to send requests to your local API.
* **Integrate with a Client**: Start developing your React Native mobile app or web frontend.
* **Learn about Authentication**: See the [Authentication](./authentication.md) guide for how to secure your requests.