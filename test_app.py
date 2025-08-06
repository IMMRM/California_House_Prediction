from app import app

def test_home():
    response=app.get("/")
    assert response.status_code==200