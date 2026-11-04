import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "usage.sqlite"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_usage_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS usage_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                prompt_tokens INTEGER NOT NULL,
                response_tokens INTEGER NOT NULL,
                thoughts_tokens INTEGER NOT NULL DEFAULT 0,
                total_tokens INTEGER NOT NULL,
                estimated_cost_usd REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Safely update an existing database without deleting records.
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(usage_records)").fetchall()}

        if "thoughts_tokens" not in columns:
            connection.execute(
                """
                ALTER TABLE usage_records
                ADD COLUMN thoughts_tokens INTEGER NOT NULL DEFAULT 0
                """
            )


def record_usage(
    model: str,
    prompt_tokens: int,
    response_tokens: int,
    total_tokens: int,
    thoughts_tokens: int = 0,
):
    # Estimated Gemini 3.6 Flash Standard paid-tier pricing.
    input_price_per_million = 0.75
    output_price_per_million = 3.75

    billable_output_tokens = response_tokens + thoughts_tokens

    estimated_cost_usd = (
        prompt_tokens * input_price_per_million + billable_output_tokens * output_price_per_million
    ) / 1_000_000

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO usage_records (
                model,
                prompt_tokens,
                response_tokens,
                thoughts_tokens,
                total_tokens,
                estimated_cost_usd
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                model,
                prompt_tokens,
                response_tokens,
                thoughts_tokens,
                total_tokens,
                estimated_cost_usd,
            ),
        )


def get_usage_summary() -> dict:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_requests,
                COALESCE(SUM(prompt_tokens), 0) AS total_prompt_tokens,
                COALESCE(SUM(response_tokens), 0) AS total_response_tokens,
                COALESCE(SUM(thoughts_tokens), 0) AS total_thoughts_tokens,
                COALESCE(SUM(total_tokens), 0) AS total_tokens,
                COALESCE(SUM(estimated_cost_usd), 0)
                    AS estimated_cost_usd
            FROM usage_records
            """
        ).fetchone()

    return dict(row)
