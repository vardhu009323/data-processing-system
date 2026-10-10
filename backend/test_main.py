
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Data Processing System API"
    }


def test_create_job(client):
    response = client.post(
        "/jobs",
        json={"numbers": [12, 45, 7, 23]}
    )

    assert response.status_code == 200

    body = response.json()
    assert body["status"] == "completed"
    assert body["input_size"] == 4
    assert body["result"]["maximum"] == 45
    assert body["result"]["minimum"] == 7
    assert body["result"]["sum"] == 87


def test_empty_dataset(client):
    response = client.post("/jobs", json={"numbers": []})
    assert response.status_code == 422


def test_missing_numbers(client):
    response = client.post("/jobs", json={})
    assert response.status_code == 422


def test_too_many_numbers(client):
    response = client.post(
        "/jobs",
        json={"numbers": list(range(10001))}
    )
    assert response.status_code == 422


def test_get_all_jobs(client):
    response = client.get("/jobs")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_job_by_id(client):
    create_response = client.post(
        "/jobs",
        json={"numbers": [12, 45, 7, 23]}
    )

    assert create_response.status_code == 200
    job_id = create_response.json()["job_id"]

    get_response = client.get(f"/jobs/{job_id}")

    assert get_response.status_code == 200

    body = get_response.json()
    assert body["job_id"] == job_id
    assert body["status"] == "completed"
    assert body["result"]["maximum"] == 45
    assert body["result"]["minimum"] == 7
    assert body["result"]["sum"] == 87


def test_get_nonexistent_job(client):
    response = client.get("/jobs/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Job not found"}


def test_get_all_jobs_pagination(client):
    # Create three jobs
    for numbers in ([1, 2], [10, 20], [100, 200]):
        response = client.post(
            "/jobs",
            json={"numbers": list(numbers)}
        )
        assert response.status_code == 200

    response = client.get("/jobs?skip=0&limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_all_jobs_invalid_pagination(client):
    response = client.get("/jobs?skip=-1")
    assert response.status_code == 422

    response = client.get("/jobs?limit=101")
    assert response.status_code == 422
