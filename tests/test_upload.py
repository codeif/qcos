from qcos import Client


def test_ok():
    assert True, "success"


def test_params(secret_id: str | None):
    print(secret_id)
    assert secret_id, "no secret_id"


def test_client(client: Client):
    print(client)
    # assert not secret_id, f'has secret_id: {secret_id}'
    assert client, "no client"


def test_upload(client: Client):
    key = "test/cab+/abc.json"
    data = {"key": "haha"}
    resp = client.smart_put_object(key, data)
    assert resp.status_code == 200, f"resp text: {resp.text}"
