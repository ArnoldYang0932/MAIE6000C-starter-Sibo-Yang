from __future__ import annotations


def test_health_endpoints(client):
    for path in ["/", "/health/live", "/health/ready"]:
        response = client.get(path)
        assert response.status_code == 200


def test_create_and_read_case_and_job(client):
    create_response = client.post(
        "/cases",
        json={
            "title": "Cannot login to dashboard",
            "description": "User cannot access the dashboard after a password reset.",
        },
    )
    assert create_response.status_code == 201

    payload = create_response.json()
    case_id = payload["case"]["id"]
    job_id = payload["job"]["id"]

    assert payload["case"]["status"] == "queued"
    assert payload["job"]["status"] == "pending"
    assert payload["job"]["job_type"] == "triage_case"
    assert payload["job"]["case_id"] == case_id

    list_response = client.get("/cases")
    assert list_response.status_code == 200
    assert any(item["id"] == case_id for item in list_response.json())

    case_response = client.get(f"/cases/{case_id}")
    assert case_response.status_code == 200
    assert case_response.json()["title"] == "Cannot login to dashboard"

    job_response = client.get(f"/jobs/{job_id}")
    assert job_response.status_code == 200
    assert job_response.json()["case_id"] == case_id

def test_list_cases_filters_by_status(client):
    create_response = client.post(
        "/cases",
        json={
            "title": "Cannot access account",
            "description": "User cannot access the account after resetting the password.",
        },
    )
    assert create_response.status_code == 201

    case_id = create_response.json()["case"]["id"]

    queued_response = client.get("/cases", params={"status": "queued"})
    assert queued_response.status_code == 200
    assert any(item["id"] == case_id for item in queued_response.json())
    assert all(item["status"] == "queued" for item in queued_response.json())

    triaged_response = client.get("/cases", params={"status": "triaged"})
    assert triaged_response.status_code == 200
    assert all(item["id"] != case_id for item in triaged_response.json())


def test_list_cases_rejects_invalid_status(client):
    response = client.get("/cases", params={"status": "not-a-valid-status"})

    assert response.status_code == 422
