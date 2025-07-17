# Authentication System Documentation

## Overview
The application uses JWT (JSON Web Token) authentication powered by:
- `dj-rest-auth` for authentication endpoints
- `django-allauth` for registration
- `SimpleJWT` for token handling

---

## Table of Contents  
1. [Authentication Flow](#authentication-flow)  
2. [User Model](#user-model)  
3. [API Endpoints](#api-endpoints)  
   - 3.1 [Registration](#registration)  
   - 3.2 [Login](#login)  
4. [Configuration Details](#configuration-details)  
5. [Client Implementation Guide](#client-implementation-guide-react-native)  
6. [Business User Considerations](#business-user-considerations)  

---

## Authentication Flow
1. User registers via `/register` endpoint
2. User logs in via `/login` to obtain JWT tokens
3. Access token is included in subsequent requests
4. When access token expires, client refreshes it using `/token/refresh`

## User Model

Using login is using `email`. `username` is still present (optional) but not the primary field for authentication.
The custom user model extends Django's `AbstractUser` with additional fields:
- `is_business_user`: Boolean indicating if user belongs to a business customer
- `is_company_admin`: Boolean indicating admin privileges for business users
- `agreed_to_terms`: Boolean required at registration
- `full_name`: Automatically generated from first_name and last_name
- `phone_number`: Optional field for user contact
- `email`: Used as primary identifier for login (see below)

## API Endpoints

### Registration
- **URL**: `/register`
- **Method**: POST
- **Description**: Creates a new user account
- **Required Fields**:
      - `email`: Must be unique
      - `password1, password2`: Minimum 8 characters, cannot be too common or entirely numeric
      - `first_name, last_name`: Required
      - `agreed_to_terms`: Must be true

- **Response**: Returns JWT tokens on successful registration

### Login
- **URL**: `/login`
- **Method**: POST
- **Description**: Authenticates user and returns JWT tokens
- **Required Fields**: username/email, password
- **Response**: 
  ```json
  {
    "access": "access_token",
    "refresh": "refresh_token",
    "user": {user_details}
  }
  ```

### Logout
- **URL**: `/logout`
- **Method**: POST
- **Description**: Invalidates the refresh token (if using token rotation)

### User Details
- **URL**: `/user`
- **Method**: GET
- **Description**: Returns authenticated user's details
- **Authentication**: JWT required

### Token Verification
- **URL**: `/token/verify`
- **Method**: POST
- **Description**: Validates an access token
- **Required Fields**: token

### Token Refresh
- **URL**: `/token/refresh`
- **Method**: POST
- **Description**: Generates new access token using refresh token
- **Required Fields**: refresh

## Configuration Details

### JWT Settings
- Access token lifetime: 1 day
- Refresh token lifetime: 7 days
- Algorithm: HS512
- Token rotation: Disabled
- Last login updated on token refresh

### Security Notes
- CSRF protection is disabled (note the commented middleware)
- JWT HTTPONLY is set to False to allow client-side access
- Uses strong HS512 signing algorithm

## Client Implementation Guide (React Native)

### Login Flow
1. Call `/login` with credentials
2. Store received tokens securely (AsyncStorage or secure storage)
3. Include access token in Authorization header for protected requests:
   ```
   Authorization: Bearer <access_token>
   ```

### Token Refresh Flow
1. When receiving 401 responses, call `/token/refresh`
2. Replace stored access token with new one
3. Retry original request with new token

### Error Handling
- Handle 401 responses by attempting token refresh
- Handle 400 responses for invalid credentials/tokens
- Provide appropriate user feedback for failed authentication

## Business User Considerations
- Business users should have `is_business_user` set to True
- Company admins should have both `is_business_user` and `is_company_admin` set to True
- These flags can be used to gate business-specific functionality
