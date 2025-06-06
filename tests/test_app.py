from http import HTTPStatus

from fastapi.testclient import TestClient

from domus_backend.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'Message': 'Olá Mundo!'}


def test_post_admin_deve_criar_admin():
    client = TestClient(app)
    payload = {
        "nome": "Admin Teste",
        "email": "admin@teste.com",
        "senha": "senha123"
    }

    response = client.post("/admin/", json=payload)
    print(response.status_code)
    print(response.json())

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data["nome"] == "Admin Teste"
    assert data["email"] == "admin@teste.com"
    assert data["tipo"] == "Administrador"
    assert "id" in data