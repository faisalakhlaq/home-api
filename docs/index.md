# Developer Documentation for Balkan API

Welcome to the official developer documentation for the Balkan API! This API provides the backend services for a real estate application, enabling robust CRUD operations for properties, user management and favorite listings.

This documentation is designed to help you quickly integrate your applications (mobile, web, or other services) with the Balkan API.

---

## Quick Links

* **[Getting Started](./getting-started/installation.md)**: Set up your environment and make your first API call.
* **[API Reference](./api-reference/properties.md)**: Explore all available endpoints, request/response formats, and examples.
* **[Authentication](./getting-started/authentication.md)**: Learn how to authenticate your requests securely.
* **[Data Models](./concepts/data-models.md)**: Understand the core data structures used in the API.

---

## Table of Contents

1.  **Getting Started**
    * [Installation & Setup](./getting-started/installation.md)
    * [Authentication](./getting-started/authentication.md)
    * [Testing the API](./getting-started/testing.md)

2.  **API Reference**
    * [Properties API](./api-reference/properties.md)
        * [`GET /properties/`](./api-reference/properties.md#list-properties)
        * [`GET /properties/{id}/`](./api-reference/properties.md#retrieve-property)
        * [`POST /properties/`](./api-reference/properties.md#create-property)
        * `PUT /properties/{id}/`
        * [`DELETE /properties/{id}/`](./api-reference/properties.md#not-allowed)
    * [User API](./api-reference/users.md)
    * [Favorites API](./api-reference/favorites.md)
    * [Search API](./api-reference/search.md)
    * [Common Response Formats](./api-reference/common-responses.md)

3.  **Core Concepts**
    * [Data Models & Schemas](./concepts/data-models.md)
    * [Authentication Methods](./concepts/authentication-methods.md)
    * [Error Handling & Status Codes](./concepts/error-handling.md)
    * [Pagination & Filtering](./concepts/pagination-filtering.md)

4.  **Tutorials**
    * [How to Register a New User](./tutorials/register-user.md)
    * [How to Add a Property to Favorites](./tutorials/add-favorite.md)
    * [How to Upload Property Images](./tutorials/upload-property-images.md)

5.  **Deployment**
    * [PythonAnywhere Deployment Guide](./deployment/pythonanywhere.md)

6.  **Additional Resources**
    * [Release Notes](./release-notes.md)
    * [Contributing to Balkan API](./contribute.md)
    * [Support & Contact](#) *(Link to a support email or forum)*
