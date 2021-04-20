# Design Draft Document

_Advanced Web Frameworks_

Kai Prince, Philip Arff, Gabriel Stewart
 7952807, 6309850, 6989727
April 20, 2021

# Project Requirements

This is a front end and user management service to display and edit point clouds

## Front end

- Point cloud visualization.
- User account creation and management
- User security

## Back end

- User database
- Authentication

## Not required

- Real-time communication (web sockets)
- CDN

# Plan for API endpoints

## Back end

### User

- Base: /api/user
- GET: /{id}
  - Headers:
    - Auth Token (JWT)
  - Body:
    - None
  - Returns:
    - Username
    - Email
- DELETE: /{id}
  - Headers:
    - Auth Token (JWT)
  - Body:
    - None
  - Returns:
    - None
- PUT: /{id}
  - Headers:
    - Auth Token (JWT)
  - Body:
    - Username
    - Email
  - Returns:
    - None
- POST: /new
  - Body:
    - Username
    - Email
  - Returns:
    - ID

### Authentication

- Base: /api/auth
- POST: /login
  - Body:
    - Username
    - Password
  - Returns:
    - Auth token (JWT)
- DELETE: /{user\_id}
  - Headers:
    - Auth Token (JWT)
  - Body:
    - None
  - Returns:
    - None
- PUT: /{user\_id}
  - Headers:
    - Auth Token (JWT)
  - Body:
    - Password
  - Returns:
    - None
- POST: /new
  - Body:
    - Username
    - Password
  - Returns:
    - None

# Architecture decisions

## Front end

### Libraries

- React
- js for point cloud visualization
- JWT for authentication token

## Back end

### Libraries

- Django REST framework
- JWT for Django

### Database

- PostgreSQL provided by Heroku.
- For security, non-sequential IDs will be used.

### Cloud platform

- GitHub actions for CI
- Heroku for hosting

### Other optional services

- Management provided by Django&#39;s built-in admin.
