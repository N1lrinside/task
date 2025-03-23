from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.utils import decrypt_password

client = TestClient(app)


def setup_module(module):
    Base.metadata.create_all(bind=engine)


def teardown_module(module):
    Base.metadata.drop_all(bind=engine)


def test_create_password():
    response = client.post("/password/test_service", json={"password": "test123"})
    assert response.status_code == 200
    assert response.json() == {"service_name": "test_service", "password": "test123"}


def test_get_password():
    response = client.get("/password/test_service")
    assert response.status_code == 200

    encrypted_password = response.json()["password"]
    decrypted_password = decrypt_password(encrypted_password)
    assert decrypted_password == "test123"