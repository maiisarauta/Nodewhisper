import pytest

@pytest.mark.asyncio
async def test_wallet_crud(client, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    res = await client.post(
        "/api/v1/wallets/",
        headers=headers,
        json={
            "address": "0xTEST123",
            "label": "Test Wallet"
        }
    )

    assert res.status_code == 200
    wallet_id = res.json()["id"]

    res = await client.get(
        "/api/v1/wallets/",
        headers=headers
    )

    assert res.status_code == 200
    assert len(res.json()) >= 1
