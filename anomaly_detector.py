
import pandas as pd


def detect_anomalies(df):
    df = df.copy()

    resolution_threshold = df["resolution_time_hrs"].quantile(0.95)

    df["ticket_age_hrs"] = (
        df["created_at"].max() - df["created_at"]
    ).dt.total_seconds() / 3600

    df["is_anomaly"] = (
        (df["resolution_time_hrs"] > resolution_threshold)
        |
        (
            df["priority"].isin(["High", "Critical"])
            & (df["status"] != "Resolved")
            & (df["ticket_age_hrs"] > 24)
        )
    )

    return df[df["is_anomaly"]].copy()


def get_anomaly_summary(df):
    anomalies = detect_anomalies(df)

    return {
        "anomaly_count": len(anomalies),
        "resolution_threshold_95": round(
            df["resolution_time_hrs"].quantile(0.95), 2
        )
    }
