"""test endpoint"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from jpzipcode.fastapi.endpoint import create_endopoint

app = FastAPI()

app.get("/zip")(create_endopoint())


def test_endpoint():
    """Test endpoint"""
    zip_code = "5650871"
    client = TestClient(app)
    res = client.get(f"/zip?zipcode={zip_code}")
    result = res.json()
    assert res.status_code == 200
    assert result[0]["address"]["prefecture"] == "大阪府"
    assert result[0]["address"]["city"] == "吹田市"
    assert result[0]["address"]["town"] == "山田丘"
