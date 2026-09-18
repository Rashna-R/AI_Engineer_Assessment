import pandas as pd

from data_loader import load_data
from anomaly_detector import detect_anomalies, get_anomaly_summary
from llm_handler import ask_llm, detect_intent


df = load_data()


def get_open_tickets():
    return int((df["status"] == "Open").sum())


def get_anomaly_data():
    return detect_anomalies(df)


def get_average_rating(category=None):
    data = df.copy()

    if category:
        data = data[data["category"].str.lower() == category.lower()]

    return round(float(data["customer_rating"].mean()), 2)


def get_top_resolving_agent():
    resolved = df[df["status"] == "Resolved"]

    result = (
        resolved.groupby("agent_id")
        .size()
        .sort_values(ascending=False)
    )

    if result.empty:
        return None

    return {
        "agent_id": result.index[0],
        "resolved_tickets": int(result.iloc[0])
    }


def get_critical_not_resolved_12h():
    data = df.copy()

    data["ticket_age_hrs"] = (
        df["created_at"].max() - df["created_at"]
    ).dt.total_seconds() / 3600

    result = data[
        (data["priority"] == "Critical") &
        (
            (data["status"] != "Resolved") &
            (data["ticket_age_hrs"] > 12)
            |
            (data["status"] == "Resolved") &
            (data["resolution_time_hrs"] > 12)
        )
    ]

    return result


def execute_query(user_query):
    intent = detect_intent(user_query)

    query_lower = user_query.lower()

    if intent == "count":
        if "open" in query_lower:
            return get_open_tickets()

        if "critical" in query_lower:
            return len(get_critical_not_resolved_12h())

        return len(df)

    elif intent == "agent":
        return get_top_resolving_agent()

    elif intent == "anomaly":
        return get_anomaly_summary(df)

    elif intent == "average_rating":
        category = None

        for cat in df["category"].unique():
            if cat.lower() in query_lower:
                category = cat
                break

        return get_average_rating(category)

    elif intent == "filtered_tickets":
        if "critical" in query_lower and "12" in query_lower:
            result = get_critical_not_resolved_12h()

            return result[
                [
                    "ticket_id",
                    "priority",
                    "status",
                    "created_at",
                    "resolution_time_hrs"
                ]
            ].to_dict(orient="records")

        return []

    return "I could not understand the query."


def answer_query(user_query):
    data_result = execute_query(user_query)

    answer = ask_llm(user_query, data_result)

    return {
        "question": user_query,
        "intent": detect_intent(user_query),
        "data": data_result,
        "answer": answer
    }


# Weekly anomaly support
def get_weekly_anomaly_data():
    latest_date = df["created_at"].max()
    week_start = latest_date - pd.Timedelta(days=7)

    weekly_data = df[
        (df["created_at"] >= week_start) &
        (df["created_at"] <= latest_date)
    ].copy()

    weekly_data["ticket_age_hrs"] = (
        (latest_date - weekly_data["created_at"]).dt.total_seconds() / 3600
    )

    threshold = df["resolution_time_hrs"].quantile(0.95)

    weekly_anomalies = weekly_data[
        (weekly_data["resolution_time_hrs"] > threshold) |
        (
            weekly_data["priority"].isin(["High", "Critical"]) &
            (weekly_data["status"] != "Resolved") &
            (weekly_data["ticket_age_hrs"] > 24)
        )
    ].copy()

    return weekly_anomalies


_original_answer_query = answer_query

def answer_query(question):
    q = question.lower()

    if "anomal" in q and ("week" in q or "7 day" in q):
        result = get_weekly_anomaly_data()
        count = len(result)

        return {
            "question": question,
            "intent": "weekly_anomaly",
            "data": count,
            "answer": f"There are {count} anomalies in resolution times this week."
        }

    return _original_answer_query(question)
