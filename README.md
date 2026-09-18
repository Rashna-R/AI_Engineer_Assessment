# AI Support Ticket Analytics

An AI-powered customer support ticket analytics system built with Python, Pandas, FastAPI, and Groq LLM.

## Features

- CSV ingestion and data analysis
- Natural-language ticket queries
- AI-powered intent detection
- Anomaly detection
- REST API
- Minimal web UI
- Health check endpoint

## Architecture

CSV Dataset
    |
    v
Data Loader
    |
    v
Pandas Data Processing
    |
    +--> Query Engine
    |       |
    |       v
    |     Groq LLM
    |
    +--> Anomaly Detector
    |
    v
FastAPI
    |
    +--> REST API
    |
    +--> Minimal Web UI

## API Endpoints

### Health Check

GET `/health`

### Natural Language Query

POST `/query`

Example:

{
    "question": "How many tickets are currently open?"
}

### Anomaly Detection

GET `/anomalies`

## Example Questions

- How many tickets are currently open?
- Which agent resolved the most tickets?
- What is the average customer rating for Technical category tickets?
- Show me all Critical tickets not resolved within 12 hours.
- Are there any anomalies in resolution times?

## Technology

- Python
- Pandas
- FastAPI
- Groq LLM
- Pydantic
- Uvicorn

## Setup

1. Install dependencies:

`pip install -r requirements.txt`

2. Create a `.env` file:

`GROQ_API_KEY=your_groq_api_key`

`GROQ_MODEL=your_available_groq_model`

3. Start the application:

`python run.py`

4. Open:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

## LLM Design

The LLM is used for natural-language understanding and intent detection.

Actual numerical results are calculated using deterministic Pandas operations before being passed to the LLM for response generation. This reduces the risk of hallucinated statistics.

## Anomaly Detection

The system flags:

1. Tickets with unusually long resolution times using the 95th percentile threshold.
2. High or Critical priority unresolved tickets older than 24 hours.

For historical dataset analysis, ticket age is calculated relative to the latest timestamp available in the dataset.

## Limitations

- The dataset is a static CSV file.
- Time-based queries are relative to the available dataset timestamps.
- The system currently supports a defined set of analytics intents.
- Production deployment would require authentication, persistent storage, logging, monitoring, and stronger input validation.

## Project Structure

AI_Engineer_Assessment/

- support_tickets.csv
- data_loader.py
- anomaly_detector.py
- llm_handler.py
- main.py
- app.py
- run.py
- requirements.txt
- README.md
- .env
- .gitignore
- exploration.ipynb
