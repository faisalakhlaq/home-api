# API Reference: Auto-Generated Documentation

Welcome to the API reference for the Balkan Home Backend API\!

For the most accurate, up-to-date, and interactive documentation of our API endpoints, including detailed request/response schemas, available parameters and example payloads, please refer to our auto-generated documentation portals:

## 1\. Swagger UI

The Swagger UI provides a comprehensive and interactive interface where you can:

  * Explore all available API endpoints and their associated HTTP methods.
  * View detailed schemas for request bodies, response payloads, and error messages.
  * Understand required headers (e.g., for authentication).
  * Even make test API calls directly from your browser to see live responses.

##### Access Swagger UI:

  * Development (Local): [Localhost](http://localhost:8000/api/v1/schema/swagger-ui/)
  * Production: [Production Swagger URL](https://faisalakhlaq.pythonanywhere.com/api/v1/swagger-ui/)

## 2\. ReDoc

ReDoc offers an alternative, highly readable, and single-page documentation experience. It's particularly well-suited for quickly scanning through the entire API and understanding the overall structure.

##### Access ReDoc:

  * Development (Local): [Localhost](http://localhost:8000/api/v1/schema/redoc/)
  * Production: [Production ReDoc URL](https://faisalakhlaq.pythonanywhere.com/api/v1/properties/properties/1/)

## How is this documentation generated?

Our API documentation is dynamically generated directly from the backend codebase using [Django REST Framework Spectacular](https://drf-spectacular.readthedocs.io/en/latest/). This approach ensures that the documentation is always synchronized with the actual API implementation, minimizing discrepancies and outdated information.

Key details like:

  * Endpoint paths and HTTP methods
  * Request parameters (path, query, header)
  * Request body schemas
  * Response schemas for various HTTP status codes
  * Field-level descriptions (derived from serializer `help_text` and docstrings)
  * Filtering options (from `django-filter` integration)

...are automatically inferred from our Django REST Framework `ViewSets` and `Serializers`.

## When to use this manual documentation?

This `docs/` folder, including this document, serves as a complementary resource for:

  * **Getting Started:** How to set up and run the project locally.
  * **Conceptual Overviews:** High-level explanations of architectural patterns, design principles, and core concepts.
  * **Authentication & Authorization:** Detailed workflows and security considerations.
  * **General API Conventions:** Information on error handling, pagination, or specific custom behaviors not easily conveyed in a schema.
  * **Contributing:** Guidelines for backend development.
