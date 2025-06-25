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

### Features

#### Technology Stack
- **Framework**: Flask
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **File Type Detection**: python-magic
  - The file type is determined not only by the file extension but also by analyzing its contents.
<hr>

### Security Considerations
- File types are verified by content, not just extension
- Download URLs are encrypted and have a short expiration time
- User passwords are hashed before storage
<hr>

### API Endpoints
#### Authentication
- **POST** `/signup`: Sign up a new user
- **GET** `/verify-email/<token>`: Verify user's email
- **POST** `/login`: Log in a user

#### File Operations
- **POST** `/upload`: Upload a file (Operation Users only)
- **GET** `/files`: List all uploaded files
- **GET** `/download/<file_id>`: Generate a download link for a file
- **GET** `/secure-download/<token>`: Download a file using a secure token
<hr>

### Future Improvements
- Implement rate limiting
- Add file encryption at rest
- Implement more granular user permissions
- Add logging and monitoring
<hr>

### Testing
To run the test suite:
```shell
pytest -v tests/
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/premkumarthouda/Secure_file_sharing_system
cd Secure_file_sharing_system
2. Set up a virtual environment:
   ```shell
   python -m venv venv
   ./venv/Scripts/activate  # On Linux use `source venv\bin\activate`
   ```
3. Install dependencies:
   ```shell
   pip install -r requirements.txt
   pip install python-magic-bin~=0.4.14 # only for Windows 
   sudo apt update && sudo apt install -y libmagic-dev # only for Linux
   ```
4. Set up environment variables:<br>
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   MONGO_URI=your_mongodb_uri
   UPLOAD_FOLDER=path_to_upload_folder
   SMTP2GO_API_KEY=your_smtp2go_api_key
   SMTP2GO_SENDER='sender_name <sender_email>'
   BASE_URL='' # specify the base URL of your application or leave empty for 127.0.0.1:5000
   ```
5. Run the application:
   ```shell
   python run.py
   ```
<hr>

### Deployment
Follow these steps to deploy the application using Docker
1. Create a Dockerfile <br>
   Create a file named `Dockerfile` in the root directory of the project with the following content:
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /SFSS
   COPY . .
   RUN pip install -r requirements.txt
   RUN apt update && apt install -y libmagic-dev
   RUN pip install waitress
   RUN mkdir uploads
   EXPOSE 5000
   CMD ["waitress-serve", "--port=5000", "--call", "app:create_app"]
   ```

2. Create a .dockerignore file <br>
   Create a `.dockerignore` file in the root directory to exclude unnecessary files:
   ```
   .idea/
   venv/
   .pytest_cache
   *.pyc
   __pycache__/
   .git/
   .gitignore
   uploads/
   tests/
   README.md
   Dockerfile
   .dockerignore
   ```
3. Build the Docker image <br>
   Run the following command in your terminal:
    ```shell 
    sudo docker build -t sfss .
    ```

4. Run the Docker container <br>
   To run the container with a mounted volume, use:
    ```shell
    sudo docker run --name sfss -d -p 5000:5000 -v $(pwd)/uploads:/uploads sfss
    ```
    This command does the following: <br>
    **-d**: Runs the container in detached mode. This means the container will keep running in the background.<br>
    **-p 5000:5000**: Maps port 5000 of the host to port 5000 on the container. <br>
    **-v $(pwd)/uploads:/uploads**: Mounts the uploads directory from your current working directory to /uploads in the container


5. Access your application <br>
The application should now be accessible at `http://localhost:5000`
<hr>

### Contributing
This project was created as part of an assessment. However, if you have suggestions or improvements, please feel free to open an issue or submit a pull request.
<hr>

### License
MIT License


