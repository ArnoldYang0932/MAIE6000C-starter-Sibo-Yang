# Week 3 Submission — Individual Readiness Lab

## Student information

- Name: Sibo Yang
- Student ID: 21321809
- Repository: https://github.com/ArnoldYang0932/MAIE6000C-starter-Sibo-Yang
- Checkpoint tag: `w03-readiness`
- Commit SHA: Recorded in the Canvas submission and identified by the checkpoint tag.

## 1. What I changed

I added optional status filtering to the existing `GET /cases` endpoint.

The endpoint now accepts the following optional query parameter values:

- `status=new`
- `status=queued`
- `status=triaged`
- `status=failed`

For example:

```text
GET /cases?status=triaged
```

When the `status` parameter is omitted, the endpoint preserves its original
behavior and returns cases without status filtering. Invalid status values are
rejected with an HTTP 422 validation response.

## 2. Files touched

- `services/api/app/main.py`
- `tests/integration/test_api_case_flow.py`
- `submissions/week03/README.md`

## 3. How I verified it

I performed the following checks:

- Built and ran the application with Docker Compose and Python 3.11.
- Checked the API and AI service health endpoints.
- Tested the unfiltered `GET /cases` endpoint.
- Tested filtering with `status=triaged` and `status=queued`.
- Confirmed that an invalid status returns HTTP 422.
- Ran the unit and integration test suite.
- Ran Ruff lint checks.

Commands used:

```bash
docker compose exec api pytest -q tests/unit tests/integration
docker compose exec api ruff check .
curl http://localhost:8000/health/ready
curl 'http://localhost:8000/cases'
curl 'http://localhost:8000/cases?status=triaged'
curl 'http://localhost:8000/cases?status=queued'
curl -i 'http://localhost:8000/cases?status=invalid'
```

Verification results:

- Tests: `6 passed, 2 warnings`
- Ruff: `All checks passed!`
- Invalid status request: `HTTP 422 Unprocessable Entity`
- Existing unfiltered endpoint remained operational.

The two test warnings are deprecation warnings originating from third-party
Starlette and python-json-logger dependencies. They did not cause test failures.

## 4. Known limitations or notes

- The filter only accepts values defined by the existing `CaseStatus` enumeration.
- The worker processes queued cases quickly, so a manual `status=queued` request
  may return an empty list.
- Filtering can be combined with the existing `limit` parameter.
- No database migration was required because the case status field already existed.

## 5. AI Use Statement

- Tool used: OpenAI Codex
- Purpose: The tool was used to analyze the assignment requirements, propose a
  bounded implementation, and suggest integration test cases and documentation.
- Verification: I reviewed the proposed implementation, rebuilt the Docker
  services, ran the automated tests, ran Ruff, and manually verified the API
  behavior.
- Changes or rejected suggestions: I kept the change limited to the existing
  cases endpoint and did not introduce a database migration or unrelated
  architectural changes.
- Responsibility: I understand and can explain all submitted changes.