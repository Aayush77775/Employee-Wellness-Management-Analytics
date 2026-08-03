# Project Objective

The objective of Milestone 3 is to develop an AI-powered Employee Wellness Analytics system that analyzes employees' journal entries and feedback to identify their emotional state and overall sentiment. The application integrates multilingual NLP preprocessing, transformer-based emotion detection, and VADER sentiment analysis to generate meaningful wellness insights. The analyzed results are displayed through a Streamlit interface and securely stored in a PostgreSQL database for future analysis.

---

# Model Used

### Emotion Detection

* **Model:** Transformer-based BERT Emotion Classifier
* **Framework:** Hugging Face Transformers
* **Purpose:** Predicts the dominant emotion from employee journal entries.

### NLP Libraries

* spaCy
* langdetect
* deep-translator
* stopwordsiso
* ftfy
* emoji

### Sentiment Analysis

* **Library:** VADER Sentiment Analyzer

The sentiment analyzer computes:

* Positive Score
* Negative Score
* Neutral Score
* Compound Score

---

# Emotion Detection Pipeline

```text
Employee Journal Entry
        │
        ▼
Text Normalization
        │
        ▼
Language Detection
        │
        ▼
Text Cleaning
(Remove URLs, Emojis, Special Characters)
        │
        ▼
Tokenization
        │
        ▼
Stopword Removal
        │
        ▼
Translation to English (if required)
        │
        ▼
Lemmatization
        │
        ▼
Transformer Emotion Detection
        │
        ▼
Predicted Emotion
+
Confidence Score
        │
        ▼
VADER Sentiment Analysis
        │
        ▼
Store Results in PostgreSQL
        │
        ▼
Display Wellness Recommendation
```

---

# Confidence Score Calculation

The transformer model predicts probabilities for all supported emotions.

The emotion with the highest probability is selected as the predicted emotion, while its probability value is displayed as the confidence score.

**Example**

| Emotion | Confidence |
| ------- | ---------: |
| Joy     |      98.7% |

A higher confidence score indicates that the model is more certain about its prediction.

---

# Sentiment Analysis

The project uses the **VADER (Valence Aware Dictionary and Sentiment Reasoner)** model to analyze the emotional polarity of journal entries.

The following sentiment scores are calculated:

| Score    | Description                          |
| -------- | ------------------------------------ |
| Positive | Positive emotion present in the text |
| Negative | Negative emotion present in the text |
| Neutral  | Neutral content in the text          |
| Compound | Overall sentiment score (-1 to +1)   |

The compound score is stored in the database and is used to understand the employee's overall emotional state.

---

# Database Schema

## Users Table

| Column        |
| ------------- |
| id            |
| username      |
| email         |
| password_hash |
| created_at    |

---

## Journal / Mood Logs Table

| Column                  |
| ----------------------- |
| id                      |
| user_id                 |
| journal_text            |
| detected_language       |
| predicted_emotion       |
| confidence_score        |
| positive_score          |
| negative_score          |
| neutral_score           |
| compound_score          |
| wellness_recommendation |
| created_at              |

---

# API Endpoints

The backend is implemented using **FastAPI**.

| Method | Endpoint   | Description                                      |
| ------ | ---------- | ------------------------------------------------ |
| POST   | `/upload`  | Upload employee feedback or journal              |
| POST   | `/analyze` | Perform emotion detection and sentiment analysis |
| POST   | `/chat`    | Generate wellness chatbot response               |
| GET    | `/docs`    | FastAPI Swagger Documentation                    |

---

# Sample Input & Output

## Sample Input

```text
I had a stressful day because of my workload, but after completing my tasks I feel much more relaxed and confident.
```

---

## Sample Output

| Field                   | Result                                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------------ |
| Detected Language       | English                                                                                    |
| Predicted Emotion       | Joy                                                                                        |
| Confidence Score        | 96.4%                                                                                      |
| Positive Score          | 0.58                                                                                       |
| Negative Score          | 0.14                                                                                       |
| Neutral Score           | 0.28                                                                                       |
| Compound Score          | 0.76                                                                                       |
| Wellness Recommendation | Maintain a healthy work-life balance and continue practicing stress management techniques. |

---

# Observations

* Multilingual preprocessing enables the system to analyze journal entries written in different languages.
* Transformer-based emotion detection provides accurate emotion classification compared to traditional methods.
* VADER sentiment analysis effectively measures the emotional polarity of journal entries.
* Confidence scores improve the interpretability of emotion predictions.
* PostgreSQL securely stores journal analytics for future wellness monitoring.
* The Streamlit frontend and FastAPI backend provide an interactive and scalable architecture.

---
### Technologies Used

* Python
* Streamlit
* FastAPI
* PostgreSQL (Neon)
* Hugging Face Transformers
* PyTorch
* spaCy
* VADER Sentiment Analyzer
* JWT Authentication
* Google Colab
