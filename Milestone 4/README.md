# 🧠 Mood Mentor — Employee Wellness Management Analytics

Mood Mentor is an AI-powered Employee Wellness Management Analytics platform designed to help employees understand, track, and improve their emotional well-being.

The system integrates **text preprocessing, multilingual language detection, sentiment analysis, emotion detection, personalized recommendations, PostgreSQL database storage, authentication, wellness chat, dashboard analytics, and PDF report generation** into one application.

---

## 📌 Project Overview

Mood Mentor provides an integrated workflow for analyzing employee feedback and monitoring emotional wellness.

### Complete System Workflow

```text
Text / File Input
        ↓
Preprocessing
        ↓
Language Detection
        ↓
Text Cleaning
        ↓
Tokenization
        ↓
Stopword Filtering
        ↓
Translation
        ↓
Lemmatization
        ↓
Sentiment Analysis
        ↓
Emotion Detection
        ↓
Recommendation Engine
        ↓
PostgreSQL Database
        ↓
Dashboard & Analytics
        ↓
PDF Report
```

The application supports both **direct text input** and **CSV/TXT file-based input** through the Streamlit frontend and FastAPI backend.

---



# ✨ Key Features

## 🔐 1. Authentication

Mood Mentor provides a complete authentication workflow.

Features include:

* User registration
* Employee and Manager roles
* Email verification through OTP
* Login
* Password validation
* Forgot password
* Password reset
* JWT-based authentication
* Session management
* Logout

Passwords are stored using password hashing rather than plain-text storage.

The authentication workflow uses PostgreSQL for storing user and OTP information.

---

# 🧠 2. Multilingual NLP Pipeline

The NLP pipeline is implemented in:

```text
nlp_pipeline.py
```

The pipeline follows:

```text
Normalize
   ↓
Detect Language
   ↓
Clean Text
   ↓
Tokenize
   ↓
Remove Stopwords
   ↓
Translate to English
   ↓
Lemmatize
   ↓
Sentiment Analysis
   ↓
Emotion Detection
```

The implementation uses:

* `ftfy` for text normalization
* `langdetect` for language detection
* `emoji` for emoji handling
* `spaCy` for tokenization and linguistic processing
* `stopwordsiso` for multilingual stopword filtering
* `deep-translator` for translation
* `VADER` for sentiment analysis
* BERT/GoEmotions for emotion classification

The pipeline supports multiple languages and maps detected languages to readable language names.

---

# 😊 3. Emotion Detection

The project uses:

```text
bhadresh-savani/bert-base-go-emotion
```

for emotion classification.

The model provides detailed GoEmotions predictions which are mapped into the application's six main emotion categories:

| Application Emotion | Examples                                          |
| ------------------- | ------------------------------------------------- |
| 😊 Happy            | Joy, amusement, excitement, love, gratitude       |
| 😢 Sad              | Sadness, disappointment, grief, remorse           |
| 😫 Stress           | Nervousness, embarrassment, confusion             |
| 😠 Angry            | Anger, annoyance, disgust, disapproval            |
| 😨 Fear             | Fear                                              |
| 😐 Neutral          | Neutral, realization, surprise, curiosity, desire |

Emotion confidence is also calculated and returned by the pipeline.

---

# 💭 4. Sentiment Analysis

Sentiment analysis is performed using **VADER**.

The system generates sentiment scores including:

* Positive score
* Negative score
* Neutral score
* Compound score

The compound score is used to determine the final sentiment:

```text
Compound >= 0.05
        ↓
     Positive

Compound <= -0.05
        ↓
     Negative

Otherwise
        ↓
     Neutral
```

The final sentiment is combined with the detected emotion before generating recommendations.

---

# 🌱 5. Recommendation Engine

The recommendation engine is implemented separately in:

Recommendations are generated according to:

* Detected emotion
* Emotion confidence
* Final sentiment
* Compound sentiment score

The application provides wellness-oriented recommendations for different emotional states.

The recommendation engine also handles situations where the emotion classifier produces `Neutral` while the sentiment analysis indicates strongly negative sentiment.

---

# 🗄️ 6. PostgreSQL Database

The application uses **PostgreSQL** for persistent storage.



### Mood history stores information such as:

* User ID
* Mood date
* Sentiment
* Emotion
* Compound score
* Emotion confidence
* Journal text
* Source
* Creation timestamp

Database indexes are also used for user/date-based mood-history queries.

The supplied notebook demonstrates successful PostgreSQL initialization:
---

# 👥 7. Manager Dashboard

Manager users can view employee wellness information.

The manager report includes:

* Employee name
* Email
* Latest mood
* Date
* Time
* Emotion
* Team mood trend

The system also provides a team mood trend based on employee mood history.


---

# 🧩 Technology Stack

| Layer                   | Technology                    |
| ----------------------- | ----------------------------- |
| Frontend                | Streamlit                     |
| Backend                 | FastAPI                       |
| Database                | PostgreSQL                    |
| Authentication          | JWT + bcrypt                  |
| NLP                     | spaCy                         |
| Language Detection      | langdetect                    |
| Translation             | deep-translator               |
| Sentiment Analysis      | VADER                         |
| Emotion Detection       | BERT / GoEmotions             |
| Wellness Chat           | Qwen2.5-0.5B-Instruct         |
| Data Processing         | Python                        |
| Visualization           | Matplotlib / Streamlit charts |
| PDF Reports             | ReportLab                     |
| Development Environment | Google Colab                  |
| API Server              | Uvicorn                       |

---

-



# 🗄️ PostgreSQL Configuration

Create a PostgreSQL database and configure the application through environment variables.

Example:

```env
DB_HOST=your_database_host
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password

JWT_SECRET=your_jwt_secret

SMTP_EMAIL=your_email
SMTP_APP_PASSWORD=your_email_app_password
```

**Never place real credentials inside the source code or GitHub repository.**

---

# 🔐 Security

The following sensitive information must never be committed to GitHub:

* Database passwords
* Database usernames where sensitive
* API keys
* JWT secrets
* SMTP passwords
* Ngrok authentication tokens
* Private employee information
* Real employee journal entries



# 🧪 Testing



The following test cases should be verified before final submission.

| Category       | Test Case               | Expected Result               |
| -------------- | ----------------------- | ----------------------------- |
| Registration   | Valid user registration | Account created               |
| Registration   | Invalid password        | Registration rejected         |
| OTP            | Valid OTP               | Account verified              |
| OTP            | Invalid OTP             | Verification rejected         |
| OTP            | Expired OTP             | Verification rejected         |
| Login          | Correct credentials     | User logged in                |
| Login          | Incorrect credentials   | Login rejected                |
| Session        | Valid JWT               | Protected endpoint accessible |
| Session        | Invalid JWT             | Request rejected              |
| Text           | Valid text              | Analysis returned             |
| Text           | Empty text              | Validation error              |
| Text           | Multilingual text       | Language detected             |
| Text           | Emoji text              | Text processed                |
| File           | Valid TXT               | File analyzed                 |
| File           | Valid CSV               | File analyzed                 |
| File           | Unsupported extension   | Error returned                |
| File           | File larger than 5 MB   | Error returned                |
| File           | Invalid UTF-8           | Error returned                |
| Database       | Save mood result        | Record stored                 |
| Database       | Retrieve history        | Records returned              |
| Recommendation | Positive emotion        | Relevant recommendation       |
| Recommendation | Negative emotion        | Relevant recommendation       |
| Dashboard      | Mood calendar           | History displayed             |
| Dashboard      | Mood distribution       | Chart displayed               |
| Dashboard      | Mood trend              | Trend displayed               |
| Dashboard      | Emotion chart           | Emotions displayed            |
| Reports        | PDF export              | PDF generated                 |
| Chat           | Valid message           | Response generated            |
| Chat           | Empty message           | Validation error              |
| Integration    | Text → Analysis → DB    | Complete workflow works       |
| Integration    | File → Analysis → DB    | Complete workflow works       |

---

# 🔄 End-to-End Integration Testing

The most important Milestone 4 test is the complete workflow:

```text
Employee
   ↓
Login
   ↓
Journal / Mood Input
   ↓
FastAPI
   ↓
Preprocessing
   ↓
Sentiment Analysis
   ↓
Emotion Detection
   ↓
Recommendation
   ↓
PostgreSQL
   ↓
Dashboard
   ↓
Historical Analytics
   ↓
PDF Report
```

Both direct text and uploaded file workflows should be tested.

---


---

# 🎯 Final System Workflow

The final Mood Mentor workflow can be summarized as:

```text
              ┌─────────────────┐
              │ Employee Login  │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ Mood / Journal  │
              │     Input       │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ FastAPI Backend │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │ NLP Preprocess  │
              └────────┬────────┘
                       ↓
          ┌────────────┴────────────┐
          ↓                         ↓
 ┌─────────────────┐       ┌─────────────────┐
 │   Sentiment     │       │     Emotion     │
 │    Analysis     │       │    Detection    │
 └────────┬────────┘       └────────┬────────┘
          └────────────┬────────────┘
                       ↓
              ┌─────────────────┐
              │ Recommendation  │
              │     Engine      │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │   PostgreSQL    │
              │    Database     │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │    Dashboard    │
              │    Analytics    │
              └────────┬────────┘
                       ↓
              ┌─────────────────┐
              │   PDF Report    │
              └─────────────────┘
```
