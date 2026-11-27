import pytest


def create(client, **fields):
    payload = {"title": "Write report", **fields}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    return response.json()


# --- Success cases ---------------------------------------------------------


def test_create_task_returns_201(client):
    response = client.post("/tasks", json={"title": "Write report"})

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Write report"
    assert body["status"] == "todo"


def test_title_is_trimmed(client):
    body = create(client, title="  Write report  ")

    assert body["title"] == "Write report"


def test_list_tasks_returns_all_tasks(client):
    create(client, title="First")
    create(client, title="Second")

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["First", "Second"]


def test_patch_status_changes_only_status(client):
    task = create(client, description="Draft for Monday")

    response = client.patch(f"/tasks/{task['id']}", json={"status": "done"})

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "done"
    assert body["title"] == task["title"]
    assert body["description"] == task["description"]


def test_delete_returns_204_then_get_returns_404(client):
    task = create(client)

    assert client.delete(f"/tasks/{task['id']}").status_code == 204
    assert client.get(f"/tasks/{task['id']}").status_code == 404


# --- Failure cases: request body -------------------------------------------


def test_invalid_status_is_rejected(client):
    response = client.post(
        "/tasks", json={"title": "Write report", "status": "invalid"}
    )

    assert response.status_code == 422


def test_blank_title_is_rejected(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_missing_title_is_rejected(client):
    response = client.post("/tasks", json={"description": "No title"})

    assert response.status_code == 422


def test_too_long_title_is_rejected(client):
    response = client.post("/tasks", json={"title": "x" * 201})

    assert response.status_code == 422


def test_too_long_description_is_rejected(client):
    response = client.post(
        "/tasks", json={"title": "Write report", "description": "x" * 2001}
    )

    assert response.status_code == 422


def test_null_status_on_create_is_rejected(client):
    response = client.post("/tasks", json={"title": "Write report", "status": None})

    assert response.status_code == 422


@pytest.mark.parametrize("field", ["id", "owner"])
def test_unknown_field_on_create_is_rejected(client, field):
    response = client.post("/tasks", json={"title": "Write report", field: 999})

    assert response.status_code == 422


def test_unknown_field_on_patch_is_rejected(client):
    task = create(client)

    response = client.patch(f"/tasks/{task['id']}", json={"id": 42})

    assert response.status_code == 422


@pytest.mark.parametrize("field", ["title", "status"])
def test_patch_with_null_is_rejected(client, field):
    task = create(client)

    response = client.patch(f"/tasks/{task['id']}", json={field: None})

    assert response.status_code == 422


def test_patch_with_invalid_status_is_rejected(client):
    task = create(client)

    response = client.patch(f"/tasks/{task['id']}", json={"status": "banana"})

    assert response.status_code == 422


# --- Failure cases: task_id in the path ------------------------------------


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_unknown_task_id_returns_404(client, method):
    kwargs = {"json": {"status": "done"}} if method == "patch" else {}

    response = getattr(client, method)("/tasks/999", **kwargs)

    assert response.status_code == 404


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
@pytest.mark.parametrize("task_id", ["0", "-1"])
def test_non_positive_task_id_is_rejected(client, method, task_id):
    kwargs = {"json": {"status": "done"}} if method == "patch" else {}

    response = getattr(client, method)(f"/tasks/{task_id}", **kwargs)

    assert response.status_code == 422
