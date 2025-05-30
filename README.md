#  Secure File Sharing System

A clean and practical web application for securely sharing files between two types of users — **Operations (Ops)** and **Clients**. Built with **FastAPI** and **MongoDB**, this project focuses on real-world concerns like user authentication, email verification, and role-based access control.

---

##  What This Project Does

This app makes file sharing safe and controlled by ensuring:
- Only verified users can log in
- Only Ops users can upload files
- Only the intended Client can download those files

No third-party services for authentication or file handling — it’s built from the ground up using Python and MongoDB.

---

##  Key Features

- **User Registration with Email Verification**
  - Every new user receives a unique token via email
  - Accounts must be verified before login

- **Login System**
  - Passwords are securely hashed using bcrypt
  - Only verified users can log in

- **Two User Roles**
  - **Ops** users can upload files for specific clients
  - **Client** users can view and download only their own files

- **File Upload & Download**
  - Ops users upload files specifying the client’s email
  - Clients get a neat file list and download feature

---

## ⚙ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: MongoDB (via Motor - async driver)
- **Authentication**: Custom email verification + hashed passwords
- **Frontend**: HTML/CSS/JS (integrates with backend via REST API)
- **Other Tools**: 
  - `passlib` for password hashing
  - `uuid4` for unique tokens
  - CORS middleware for frontend-backend communication

---

## How do you plan on deploying this to the production environment?
My plan for deploying the Secure File Sharing System to production:

I plan to host the application on a dependable cloud service like AWS, Google Cloud, or Heroku. To make deployment smoother and ensure the app runs consistently across different setups, I will package the backend using Docker. This containerization approach helps manage dependencies and simplifies scaling when needed.

For the database, I will rely on MongoDB Atlas, a cloud-based managed database service that handles backups, security, and performance optimization, allowing me to focus on the app itself.

To protect user data during transmission, I’ll set up HTTPS by configuring SSL certificates with Let’s Encrypt, using an NGINX reverse proxy as a secure gateway for the FastAPI application.

Sensitive information such as database credentials and email settings will be kept secure by managing them through environment variables, avoiding any hardcoded secrets.

Additionally, I will integrate monitoring and logging to track the app’s health and troubleshoot issues quickly. To streamline future updates, I plan to set up a CI/CD pipeline—most likely using GitHub Actions—to automate testing and deployment.

This deployment approach ensures the system will be reliable, secure, and easy to maintain in a production setting.
