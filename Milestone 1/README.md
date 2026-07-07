## 📌 Project

## 🚀 Features

- Home Page
- User Registration (Sign Up)
- Secure User Login
- Forgot Password using OTP Verification
- OTP Delivery via Gmail SMTP
- Password Encryption using bcrypt
- JWT-based User Authentication
- Neon PostgreSQL Database Integration
- Dashboard with CSV Upload (after successful login)
- 
## 🛠️ Technologies Used

Streamlit
Python
### Database
- Neon PostgreSQL
### Authentication
- bcrypt
- JSON Web Token (JWT)
### Email Service
- Gmail SMTP
### Python Libraries
- streamlit
- psycopg2
- bcrypt
- PyJWT
- email-validator
- python-dotenv
- pandas
- smtplib
- ssl


## ⚙️ Google Colab Setup Instructions
### Step 1

Open the Authentication.ipynb notebook in Google Colab.

### Step 2

Install the required libraries.

```python
!pip install streamlit
!pip install psycopg2-binary
!pip install bcrypt
!pip install pyjwt
!pip install email-validator
!pip install python-dotenv
!pip install pyngrok```

### Step 3

Upload all project files:

- app.py
- auth.py
- db.py
- email_utils.py
- .env (if applicable)

### Step 4

Configure your Neon PostgreSQL database credentials inside the project.

Example:

```python
DB_HOST=your_host
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

### Step 5

Configure Gmail SMTP credentials.

```python
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Step 6

Run the Streamlit application.

```python
!streamlit run app.py &
```

```python
from pyngrok import ngrok

public_url = ngrok.connect(8501)

print(public_url)
```

## 🔄 Application Workflow

1. User opens the Home Page.
2. User creates a new account.
3. User verifies their email using OTP.
4. Password is encrypted using bcrypt.
5. User information is stored securely in Neon PostgreSQL.
6. User logs in using registered credentials.
7. JWT token is generated after successful authentication.
8. User is redirected to the Dashboard.
9. User can upload CSV files.
10. If the password is forgotten, the user can reset it using OTP verification.

## 🔒 Security Features

- Password Hashing using bcrypt
- JWT-based Authentication
- OTP Email Verification
- Secure PostgreSQL Database Storage
- Session Management
- Input Validation
