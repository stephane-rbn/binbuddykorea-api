import os
from base64 import b64encode

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_bin():
    login_details = f"{os.getenv("BASIC_AUTH_TEST_USERNAME")}:{os.getenv("BASIC_AUTH_TEST_PASSWORD")}".encode(
        "utf-8"
    )
    payload = b64encode(login_details).decode("utf-8")
    auth_header = f"Basic {payload}"
    response = client.post(
        "/api/v1/bins/",
        json={
            "name_en": "Test Bin",
            "name_kr": "테스트 쓰레기통",
            "description": "Test description",
        },
        headers={"Authorization": auth_header},
    )

    assert response.status_code == 200
    bin = response.json()
    assert bin["name_en"] == "Test Bin"
    assert bin["name_kr"] == "테스트 쓰레기통"
    assert bin["description"] == "Test description"
