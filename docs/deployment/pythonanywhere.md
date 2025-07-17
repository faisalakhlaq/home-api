# PythonAnywhere API Deployment Guide

This document outlines the step-by-step process for deploying and updating your API project on PythonAnywhere.

## Table of Contents

1.  [Prerequisites](#1-prerequisites)
2.  [Pull New Changes and Update Dependencies](#2-pull-new-changes-and-update-dependencies)
3.  [Configure the WSGI File](#3-configure-the-wsgi-file)
4.  [Configure the `manage.py` File (Optional but Recommended)](#4-configure-the-managepy-file-optional-but-recommended)
5.  [Generate static files](#5-generate-static-files)
6.  [Final Deployment Steps and Verification](#6-final-deployment-steps-and-verification)
7.  [Troubleshooting](#7-troubleshooting)
8. [Environment variables](#8-environment-variables)

-----

## 1\. Prerequisites

Before you begin, ensure you have the following:

  * **PythonAnywhere Account:** An active PythonAnywhere account with a configured web app for your API.
  * **Git Repository:** Your API project code hosted on a Git repository (e.g., GitHub, GitLab, Bitbucket).
  * **Virtual Environment:** A virtual environment set up on PythonAnywhere for your web app. The console link for this can be found under the "Web" tab in the "Virtualenv" section.
  * **`requirements.txt` and `requirements-prod.txt`:** These files should be present in your project's root directory, listing all necessary Python packages for development and production, respectively.

-----

## 2\. Pull New Changes and Update Dependencies

This section details how to get the latest code and install any new dependencies.

1.  **Open a Bash Console:**

      * From the "Web" tab, you can click the "Bash" link next to your virtual environment name under the "Virtualenv" section. This will open a console with your virtual environment already activated.
      * Alternatively, navigate to the "Consoles" tab on your PythonAnywhere dashboard.
      * Click on "Bash" to open a new console.

2.  **Navigate to Your Project Directory:**

      * Verify that the virtual environment is active by checking if the prompt starts with
        ```bash
        (venv)
        ```
      * Verify you are in your home directory:
        ```bash
        (venv) $ pwd
        /home/faisalakhlaq
        ```
      * List contents to confirm your project folder exists (e.g., `home-api`):
        ```bash
        (venv) $ ls -a
        # You should see 'home-api/' listed here among other files.
        .   .bash_history  .cache  .gitconfig  .ipython  .my.cnf         .profile         .pythonstartup.py  .virtualenvs  home-api
        ..  .bashrc        .git    .gitignore  .local    .mysql_history  .python_history  .vimrc             README.txt    staticfiles

        ```
      * Change into your project directory:
        ```bash
        (venv) $ cd home-api/
        ```
      * Verify you are on the correct branch (usually `main` or `master` for deployment):
        ```bash
        (venv) $ git branch
        * main
          origin/main
        ```

3.  **Pull Latest Changes:**

    ```bash
    git pull
    ```

      * *Note:* If there are merge conflicts, resolve them locally and push the changes, then pull again.

4.  **Install/Update Python Dependencies:**

    ```bash
    pip install -r requirements.txt
    pip install -r requirements-prod.txt
    ```

      * This ensures all necessary packages are installed or updated within your virtual environment.

5.  **Run Database Migrations (if applicable):**

    ```bash
    python manage.py migrate
    ```

      * This applies any new database schema changes.

-----

## 3\. Configure the WSGI File

The WSGI (Web Server Gateway Interface) file is crucial for telling PythonAnywhere how to serve your Django application.

1.  **Locate Your WSGI File:**

      * On PythonAnywhere, your web app's WSGI file is typically located at:
        `faisalakhlaq/files/var/www/faisalakhlaq_pythonanywhere_com_wsgi.py` (The exact name will depend on your domain).
      * You can easily access and edit this file by going to your "Web" tab, scrolling down to the "Code" section, and clicking on the "WSGI configuration file" link.

2.  **Update WSGI File Content:**
    Replace the existing content with the following:

    ```python
    import os
    import sys

    # Add your project directory to the sys.path
    # This is crucial so that Python can find your project's modules
    path = "/home/faisalakhlaq/home-api" # Replace 'faisalakhlaq' with your PythonAnywhere username
    if path not in sys.path:
        sys.path.append(path)

    # Set the Django settings module for production
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings.production"

    # Import the WSGI application
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    ```

      * **Important:** Ensure `path = "/home/faisalakhlaq/home-api"` correctly reflects your PythonAnywhere username and the exact path to your project's root directory (the directory containing `manage.py`).
      * `settings.production` should point to your production settings file within your project's `settings` package.

-----

## 4\. Configure the `manage.py` File (Optional but Recommended)

It's good practice to ensure your `manage.py` file explicitly uses your production settings when run on PythonAnywhere, especially for commands like `migrate` or `createsuperuser`.

1.  **Locate Your `manage.py` File:**

      * This file is located in the root of your project directory: `/home/faisalakhlaq/home-api/manage.py`.

2.  **Update `manage.py` Content:**
    Ensure the `main()` function in your `manage.py` file sets the `DJANGO_SETTINGS_MODULE` to your production settings:

    ```python
    #!/usr/bin/env python
    """Django's command-line utility for administrative tasks."""
    import os
    import sys


    def main():
        """Run administrative tasks."""
        # Ensure production settings are used when running manage.py commands
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.production")
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)


    if __name__ == "__main__":
        main()
    ```

      * This snippet ensures that any `manage.py` commands you run (e.g., `python manage.py createsuperuser`) will use your production settings, which is typically what you want on a live server.

-----

## 5\. Generate and Serve Static Files (CSS, JS, Images)

This section details how to generate and configure your project's static files (CSS, JavaScript, images, etc.) to be served correctly on PythonAnywhere. Django's `collectstatic` command gathers all static files from your apps and any directories you specify, placing them into a single directory defined by `STATIC_ROOT`. PythonAnywhere then serves these files directly from that location.

### 5.1. Configure Django Settings

First, ensure your Django project's settings are correctly configured for static files. 

Add or verify the following settings:

```python
# settings/production.py

STATIC_URL = '/static/'

# The absolute path to the directory where Django's `collectstatic` command
# will gather all static files for deployment.
# It's best practice to place this *inside* your project directory but
# separate from your version-controlled static assets (e.g., 'static' folder in apps).
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Optional: If you have additional static files not associated with a specific app
# (e.g., global CSS/JS files), list their directories here.
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'your_custom_static_folder'),
# ]
```

  * **`STATIC_URL`**: This is the URL path (e.g., `https://faisalakhlaq.pythonanywhere.com/static/css/style.css`) that will be used to access your static files in the browser.
  * **`STATIC_ROOT`**: This specifies the *physical directory* on the server where all your static files will be collected by `collectstatic`. For PythonAnywhere, setting it to `os.path.join(BASE_DIR, 'staticfiles')` means the files will be placed in a new folder named `staticfiles` directly within your `home-api` project directory (e.g., `/home/faisalakhlaq/home-api/staticfiles/`).

### 5.2. Configure PythonAnywhere Web App

Next, you need to tell PythonAnywhere to serve files from your `STATIC_ROOT` directory at the `STATIC_URL` path.

1.  **Navigate to the "Web" tab** on your PythonAnywhere dashboard.
2.  **Scroll down to the "Static files" section.**
3.  **Add a new entry (or edit an existing one) with the following details:**
      * **URL:** `/static/` (This **must** exactly match your `STATIC_URL` from `settings.py`).
      * **Directory:** `/home/faisalakhlaq/home-api/staticfiles` (This **must** exactly match your `STATIC_ROOT` from `settings.py`. **Remember to replace `faisalakhlaq` with your actual PythonAnywhere username.**)
4.  Ensure the "Enabled" checkbox for this static file mapping is checked.

### 5.3. Generate Static Files

Now that your settings and PythonAnywhere configuration are in place, you can run the `collectstatic` command.

1.  **Open a Bash Console** (as described in [Section 2. Pull New Changes and Update Dependencies](#2-pull-new-changes-and-update-dependencies)).

2.  **Navigate to your project's root directory:**
    ```bash
    (venv) $ cd home-api/
    ```
3.  **Run the `collectstatic` command:**
    ```bash
    (venv) $ python manage.py collectstatic
    ```
      * You will be prompted to confirm if you want to overwrite existing files. Type `yes` and press Enter.
      * This command will gather all static files from your Django apps and `STATICFILES_DIRS` and copy them into the `/home/faisalakhlaq/home-api/staticfiles/` directory.

After this follow the [final deployment steps and verification](#6-final-deployment-steps-and-verification).

---

## 6\. Final Deployment Steps and Verification

After updating your code and configuration, you need to reload your web application for the changes to take effect.

1.  **Reload Your Web Application:**

      * Go to the "Web" tab on your PythonAnywhere dashboard.
      * Click the "Reload" button next to your web app's domain name. This will restart the web server and load your updated application.

2.  **Verify Deployment:**

      * Open your API's root URL in a web browser:
        ```
        https://faisalakhlaq.pythonanywhere.com/api/v1/properties/
        ```
      * Navigate to different API endpoints to ensure everything is functioning as expected. Check for:
          * Correct data retrieval.
          * Error handling (e.g., trying an invalid endpoint).
          * Any new features or bug fixes are visible.
          * Check the server logs on PythonAnywhere (under the "Web" tab, click "Error log" and "Server log") for any new errors after reloading.

-----

## 7\. Troubleshooting

If you encounter issues, here are some common troubleshooting steps:

  * **Check PythonAnywhere Logs:**
      * **Error Log:** The "Error log" (found on the "Web" tab) is your first stop for debugging. It will show Python tracebacks for any unhandled exceptions in your application.
      * **Server Log:** The "Server log" (also on the "Web" tab) provides information about the web server's activity, including requests and responses, and can sometimes reveal issues with WSGI file loading.
  * **Virtual Environment Issues:**
      * Ensure your virtual environment is correctly configured and activated when running console commands.
      * Double-check that all required packages are listed in your `requirements.txt` and `requirements-prod.txt` and are successfully installed (`pip install -r ...`).
  * **Pathing in WSGI:**
      * Carefully review the `path` variable in your `wsgi.py` file. It must point directly to your project's root directory (where `manage.py` and your main Django project folder are located).
  * **Settings Module:**
      * Verify `os.environ["DJANGO_SETTINGS_MODULE"]` in your `wsgi.py` and `manage.py` files correctly points to your production settings file (e.g., `settings.production`).
  * **Permissions:**
      * Ensure your files and directories have the correct permissions. PythonAnywhere usually handles this, but if you've manually moved files, it might be a consideration.
  * **Reload Web App:**
      * Always remember to "Reload" your web app from the "Web" tab after making any code or configuration changes.

-----

## 8\. Environment variables

The `.env` file contains the environment variables which are used by the application on pythonanywhere. The file is stored at `/home/faisalakhlaq/home-api/.env`.

If the environment variables are updated, a reload of the application is required to use the updated / new env variables.
