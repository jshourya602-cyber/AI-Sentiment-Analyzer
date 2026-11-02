# AI-Based Sentiment Analyzer

An AI-powered web application that analyzes text reviews, comments, and feedback to identify their sentiment as **Positive, Negative, or Neutral** using a pretrained Transformer model.

Built with Python, Flask, Hugging Face Transformers, PyTorch, and MongoDB.

## Features

- AI-based sentiment classification.
- Three sentiment categories: Positive, Negative, and Neutral.
- Model confidence score.
- Multiple text sources: Product Review, Social Media, Customer Feedback, and Manual.
- MongoDB integration for saving analysis history.
- Interactive dashboard with sentiment distribution.
- Recent analysis history.
- Flask health-check endpoint.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application |
| Hugging Face Transformers | Sentiment analysis model |
| PyTorch | Deep learning framework |
| MongoDB Atlas | Cloud database |
| PyMongo | MongoDB connection |
| HTML, CSS | Frontend |
| Chart.js | Dashboard visualization |

## AI Model

Model: `cardiffnlp/twitter-roberta-base-sentiment-latest`

The application uses a pretrained RoBERTa Transformer model to classify text into positive, negative, and neutral sentiments.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Sentiment-Analyzer.git
cd AI-Sentiment-Analyzer
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the environment (Windows PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure environment variables

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure:

- `SECRET_KEY`: A secure random secret.
- `MONGO_URI`: Your MongoDB Atlas connection string.
- `DATABASE_NAME`: Database name.
- `SENTIMENT_MODEL`: Hugging Face model name.
- `FLASK_DEBUG`: Set to false for normal use.

Never upload your `.env` file or database credentials to GitHub.

### 6. Run the application

```bash
python app.py
```

Open your browser:

`http://127.0.0.1:5000`

The first analysis may take several minutes because the pretrained model needs to download. An internet connection is required for the initial download.

## MongoDB Atlas Setup

1. Create a MongoDB Atlas account.
2. Create a free database cluster.
3. Create a database user.
4. Configure Network Access.
5. Copy the connection string into `MONGO_URI` in your `.env` file.

The application saves analysis history in MongoDB when the database is available.

## Project Structure

```text
AI-Sentiment-Analyzer/
│
├── app.py
├── sentiment.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── result.html
│   └── dashboard.html
│
└── static/
    └── css/
        └── style.css
```

## Limitations

- The model is primarily intended for English social-media-style text.
- Sarcasm, complex expressions, and domain-specific language may affect predictions.
- Model confidence is not a guaranteed measure of prediction accuracy.
- The first model download requires an internet connection.
- Analysis history requires a working MongoDB connection.

## Future Improvements

- User authentication.
- More language support.
- Advanced analytics and filtering.
- Exportable sentiment reports.
- Improved model evaluation using a labeled dataset.

## Project Purpose

This project demonstrates the practical integration of Natural Language Processing, Transformer-based models, Flask web development, and cloud database management.