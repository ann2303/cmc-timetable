import os

import requests
from dotenv import load_dotenv

load_dotenv()
cookies = {}
BASE_URL = "http://localhost:8000"


def set_cookie():
    """Set cookies for tests."""
    with requests.Session() as session:
        response = session.post(
            f"{BASE_URL}/auth/login/",
            data={"username": "admin", "password": os.environ["ADMIN_PASSWORD"]},
        )
        assert response.status_code == 200
        assert session.cookies.get(name="api_token") is not None
        cookies["api_token"] = session.cookies.get(name="api_token")
        


def test_main_page():
    """Test the index page."""
    if len(cookies) == 0:
        set_cookie()
    response = requests.get(f"{BASE_URL}", cookies=cookies)
    assert response.status_code == 200
    assert "Main page" in response.text


def test_login():
    """Test login to the application."""
    set_cookie()


def test_logout():
    if len(cookies) == 0:
        set_cookie()
    with requests.Session() as session:
        response = session.get(f"{BASE_URL}/auth/logout/", cookies=cookies)
        assert response.status_code == 200
        assert session.cookies.get(name="api_token") is None


def test_file_upload():
    """Test file upload."""
    if len(cookies) == 0:
        set_cookie()
    with open("../examples/timetable_example.xlsx", "rb") as file:
        with requests.Session() as session:
            response = session.post(
                f"{BASE_URL}/timetable/load",
                files={"uploaded_file": file},
                cookies=cookies,
                allow_redirects=True,
            )
            assert response.status_code == 200
            assert '<table border="1" class="dataframe">' in response.text
            assert ''
