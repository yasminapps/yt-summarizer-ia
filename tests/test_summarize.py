import pytest
from flask import Flask
from routes.summarize import summarize

@pytest.fixture
def client():
    app = Flask(__name__)
    app.add_url_rule("/summarize", view_func=summarize, methods=["POST"])
    return app.test_client()

def test_summarize_missing_url(client):
    response = client.post("/summarize", data={})
    json_data = response.get_json()
    assert response.status_code == 500
    assert "Erreur côté serveur" in json_data["summary"]