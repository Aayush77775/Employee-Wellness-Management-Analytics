# 🧠 NLP Pipeline Overview

The implemented NLP pipeline performs the following operations in sequence:

1. **Text Input**
   - Direct text input
   - Upload `.txt` files
   - Upload `.csv` files

2. **Language Detection**
   - Automatically detects the language of the input text.
   - Displays the detected language before preprocessing.

3. **Unicode Text Normalization**
   - Standardizes Unicode characters into a consistent format.

4. **Text Cleaning**
   - Removes unnecessary whitespace.
   - Eliminates unwanted special characters.

5. **URL Removal**
   - Detects and removes web links.

6. **Email Removal**
   - Removes email addresses from the text.

7. **HTML Tag Removal**
   - Cleans HTML/XML tags.

8. **Emoji Extraction and Removal**
   - Extracts emojis separately.
   - Removes emojis from the text.

9. **Punctuation Removal**
   - Removes punctuation symbols.

10. **Number Removal**
    - Removes numeric values.

11. **Lowercase Conversion**
    - Converts text to lowercase wherever applicable.

12. **Tokenization**
    - Splits text into individual words (tokens).

13. **Stop-word Removal**
    - Removes common language-specific stop words.

14. **Lemmatization**
    - Converts words to their base or dictionary form.

15. **Noise Filtering**
    - Removes remaining unwanted tokens and irrelevant characters.

16. **Final Preprocessed Text**
    - Generates clean, normalized text ready for NLP applications.

---

# 🌍 Multilingual Text Support

The preprocessing pipeline supports multiple languages using appropriate NLP libraries.

### Features

- Automatic language detection
- Language-aware stop-word removal
- Language-specific preprocessing wherever supported
- Graceful handling of unsupported languages
- Unicode-compatible text processing

---

# 🛠 Technologies and Libraries Used

## Programming Language

- Python 3

## Development Environment

- Google Colaboratory (Google Colab)

## Libraries

- pandas
- numpy
- regex (`re`)
- unicodedata
- BeautifulSoup (`bs4`)
- emoji
- nltk
- spacy
- langdetect
- string
- os

---

# ⚙ Google Colab Setup Instructions

### Step 1

Open the notebook in **Google Colab**.

### Step 2

Install the required libraries:

```python
!pip install langdetect emoji beautifulsoup4 nltk spacy
```

### Step 3

Download the required NLTK resources:

```python
import nltk

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")
```

### Step 4

Download the SpaCy language model:

```python
!python -m spacy download en_core_web_sm
```

### Step 5

Run all notebook cells sequentially.

---

# 🔄 Preprocessing Workflow

```text
User Input
      │
      ▼
Language Detection
      │
      ▼
Unicode Normalization
      │
      ▼
Text Cleaning
      │
      ▼
URL Removal
      │
      ▼
Email Removal
      │
      ▼
HTML Tag Removal
      │
      ▼
Emoji Extraction
      │
      ▼
Emoji Removal
      │
      ▼
Punctuation Removal
      │
      ▼
Number Removal
      │
      ▼
Lowercase Conversion
      │
      ▼
Tokenization
      │
      ▼
Stop-word Removal
      │
      ▼
Lemmatization
      │
      ▼
Noise Filtering
      │
      ▼
Final Preprocessed Text
```

---

# 📥 Sample Input

```text
Hello! 😊

Visit https://openai.com for more details.

You can also contact me at example@gmail.com.

<p>This is an HTML paragraph.</p>

I have 5 apples and 10 oranges.
```

---

# 📤 Sample Output

### Detected Language

```text
English
```

### Extracted Emojis

```text
😊
```

### Tokens

```text
['hello', 'visit', 'details', 'contact', 'html', 'paragraph', 'apples', 'oranges']
```

### Tokens after Stop-word Removal

```text
['hello', 'visit', 'details', 'contact', 'html', 'paragraph', 'apples', 'oranges']
```

### Lemmatized Tokens

```text
['hello', 'visit', 'detail', 'contact', 'html', 'paragraph', 'apple', 'orange']
```

### Final Preprocessed Text

```text
hello visit detail contact html paragraph apple orange
```

---

# 📊 Intermediate Outputs Displayed

The notebook displays the output after every preprocessing stage:

- ✅ Original Text
- ✅ Detected Language
- ✅ Unicode Normalized Text
- ✅ Cleaned Text
- ✅ URLs Removed
- ✅ Emails Removed
- ✅ HTML Tags Removed
- ✅ Extracted Emojis
- ✅ Text after Emoji Removal
- ✅ Punctuation Removed
- ✅ Numbers Removed
- ✅ Lowercase Text
- ✅ Tokens
- ✅ Tokens after Stop-word Removal
- ✅ Lemmatized Tokens
- ✅ Noise Filtered Tokens
- ✅ Final Preprocessed Text

---
# 🎯 Conclusion

This milestone demonstrates the implementation of a complete NLP text preprocessing pipeline with multilingual support. By systematically transforming raw textual data into a normalized and structured format, the pipeline establishes a strong foundation for various Natural Language Processing and Machine Learning applications.
