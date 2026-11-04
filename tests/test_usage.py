def test_usage_starts_at_zero(client):
    response = client.get("/usage")

    assert response.status_code == 200

    data = response.json()

    assert data["total_requests"] == 0
    assert data["total_prompt_tokens"] == 0
    assert data["total_response_tokens"] == 0
    assert data["total_tokens"] == 0


def test_usage_records_multiple_requests(client):
    from app.services.usage_service import record_usage

    record_usage(
        model="gemini-3.5-flash",
        prompt_tokens=10,
        response_tokens=20,
        total_tokens=30,
    )

    record_usage(
        model="gemini-3.5-flash",
        prompt_tokens=15,
        response_tokens=25,
        total_tokens=40,
    )

    response = client.get("/usage")
    data = response.json()

    assert data["total_requests"] == 2
    assert data["total_prompt_tokens"] == 25
    assert data["total_response_tokens"] == 45
    assert data["total_tokens"] == 70


def test_usage_calculates_estimated_cost(client):
    from app.services.usage_service import record_usage

    record_usage(
        model="gemini-3.5-flash",
        prompt_tokens=1_000_000,
        response_tokens=100_000,
        total_tokens=1_100_000,
    )

    response = client.get("/usage")
    data = response.json()

    assert data["estimated_cost_usd"] == 1.125
