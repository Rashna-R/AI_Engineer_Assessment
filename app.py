
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd

from main import answer_query, get_anomaly_data


app = FastAPI(
    title="AI Support Ticket Analytics",
    description="AI-powered customer support ticket analytics system",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Support Ticket Analytics"
    }


@app.post("/query")
def query_tickets(request: QueryRequest):
    return answer_query(request.question)


@app.get("/anomalies")
def anomalies():
    data = get_anomaly_data()

    selected = data[
        [
            "ticket_id",
            "priority",
            "status",
            "resolution_time_hrs"
        ]
    ]

    records = []

    for _, row in selected.iterrows():
        record = {}

        for column in selected.columns:
            value = row[column]

            if pd.isna(value):
                record[column] = None
            elif hasattr(value, "item"):
                record[column] = value.item()
            else:
                record[column] = value

        records.append(record)

    return {
        "anomaly_count": len(records),
        "anomalies": records
    }


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Support Ticket Analytics</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }

            input {
                width: 75%;
                padding: 12px;
                font-size: 16px;
            }

            button {
                padding: 12px 20px;
                font-size: 16px;
                cursor: pointer;
            }

            #result {
                margin-top: 25px;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 8px;
                white-space: pre-wrap;
            }
        </style>
    </head>

    <body>
        <h1>AI Support Ticket Analytics</h1>

        <p>Ask a question about the support tickets:</p>

        <input
            id="question"
            placeholder="How many tickets are currently open?"
        />

        <button onclick="askQuestion()">Ask</button>

        <div id="result">Answer will appear here...</div>

        <script>
            async function askQuestion() {
                const question = document.getElementById("question").value;

                if (!question) {
                    document.getElementById("result").innerText =
                        "Please enter a question.";
                    return;
                }

                document.getElementById("result").innerText =
                    "Processing...";

                const response = await fetch("/query", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        question: question
                    })
                });

                const data = await response.json();

                document.getElementById("result").innerText =
                    data.answer || JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """
