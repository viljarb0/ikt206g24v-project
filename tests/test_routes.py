from unittest.mock import patch


@patch("app.list_users", return_value=["ADMIN"])
@patch("app.verify", return_value=True)
def test_login_route(mock_verify, mock_list_users, client):
    response = client.post("/login", data={"id": "admin", "pw": "testpw"})
    assert response.status_code == 302  # Expect redirect on success


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data


def test_public_page(client):
    response = client.get("/public/")
    assert response.status_code == 200
    assert b"Public" in response.data

