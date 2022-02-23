from fastapi.testclient import TestClient
from calc import app

client = TestClient(app)


def testPost():
    response = client.post("/calc", json={"expr": "+100.1"})
    assert response.status_code == 200
    assert response.json() == 100.1

    response = client.post("/calc", json={"expr": "-0"})
    assert response.status_code == 200
    assert response.json() == 0

    response = client.post("/calc", json={"expr": "- 6 * 2"})
    assert response.status_code == 200
    assert response.json() == -12

    response = client.post("/calc", json={"expr": "2. / 1."})
    assert response.status_code == 200
    assert response.json() == 2

    response = client.post("/calc", json={"expr": "5 + - 4"})
    assert response.status_code == 200
    assert response.json() == 1

    response = client.post("/calc", json={"expr": "*1 + 7"})
    assert response.status_code == 400

    response = client.post("/calc", json={"expr": "4 / 3 +"})
    assert response.status_code == 400

    response = client.post("/calc", json={"expr": "5 - 4 * 2"})
    assert response.status_code == 200
    assert response.json() == 2

    response = client.post("/calc", json={"expr": "0.5-6+.5"})
    assert response.status_code == 200
    assert response.json() == -5

    response = client.post("/calc", json={"expr": "1.1111 + 2.2222 + 3.3333"})
    assert response.status_code == 200
    assert response.json() == 6.667


def testGet():
    response = client.get("/history")
    assert response.status_code == 200

    response = client.get("/history?limit=30&status=success")
    assert response.status_code == 200

    response = client.get("/history?limit=5&status=fail")
    assert response.status_code == 200

    response = client.get("/history?limit=31")
    assert response.status_code == 400

    response = client.get("/history?limit=0")
    assert response.status_code == 400

    response = client.get("/history?limit=30&status=anyone")
    assert response.status_code == 400


if __name__ == '__main__':
    testPost()
    testGet()
