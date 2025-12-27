import pytest

@pytest.mark.asyncio
async def test_case_wallet_flow(client, auth_token):
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    case = await client.post(
        "/api/v1/cases/",
        headers=headers,
        json={
            "title": "Test Case",
            "description": "Investigation"
        }
    )
    assert case.status_code == 200
    case_id = case.json()["id"]

    wallet = await client.post(
        "/api/v1/wallets/",
        headers=headers,
        json={
            "address": "0xCASEWALLET",
            "label": "Case Wallet"
        }
    )
    wallet_id = wallet.json()["id"]

    attach = await client.post(
        f"/api/v1/cases/{case_id}/wallets",
        headers=headers,
        json={
            "wallet_id": wallet_id,
            "confidence": 85,
            "note": "Linked via test",
            "source": "manual"
        }
    )

    assert attach.status_code == 200

    res = await client.get(
        f"/api/v1/cases/{case_id}/wallets",
        headers=headers
    )

    assert res.status_code == 200
    assert len(res.json()) == 1
