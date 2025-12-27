import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    register = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "auth@test.com",
            "username": "abubakar",
            "password": "abuba1234"
        }
    )
    assert register.status_code in (200, 400)

    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "auth@test.com",
            "password": "abuba1234"
        }
    )

    assert login.status_code == 200
    assert "access_token" in login.json()
