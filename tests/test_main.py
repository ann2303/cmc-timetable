import os
from pathlib import Path

import pytest
import requests
from dotenv import load_dotenv

load_dotenv()
cookies = {}
BASE_URL = "http://localhost:8000"
DOCS_URL = "http://localhost:8100"


def set_cookie(*, username: str = "admin", password: str):
    """Set cookies for tests."""
    with requests.Session() as session:
        response = session.post(
            f"{BASE_URL}/auth/login/",
            data={"username": username, "password": password},
        )
        assert response.status_code == 200
        assert session.cookies.get(name="api_token") is not None
        cookies["api_token"] = session.cookies.get(name="api_token")


def test_main_page():
    """Test the index page."""
    if len(cookies) == 0:
        set_cookie(password=os.environ["ADMIN_PASSWORD"])
    response = requests.get(f"{BASE_URL}", cookies=cookies)
    assert response.status_code == 200
    assert "Main page" in response.text


@pytest.mark.order(1)
def test_login():
    """Test login to the application."""
    set_cookie(username="Ann_Ili", password=os.environ["USER_PASSWORD"])
    set_cookie(password=os.environ["ADMIN_PASSWORD"])


def test_logout():
    if len(cookies) == 0:
        set_cookie(password=os.environ["ADMIN_PASSWORD"])
    with requests.Session() as session:
        response = session.get(f"{BASE_URL}/auth/logout/", cookies=cookies)
        assert response.status_code == 200
        assert session.cookies.get(name="api_token") is None


@pytest.mark.order(2)
def test_file_upload():
    """Test file upload."""
    if len(cookies) == 0:
        set_cookie(password=os.environ["ADMIN_PASSWORD"])
    file_path = Path(os.environ["EXAMPLES_DIRECTORY_PATH"]) / "timetable_example.xlsx"
    with open(file_path, "rb") as file:
        with requests.Session() as session:
            response = session.post(
                f"{BASE_URL}/timetable/load",
                files={"uploaded_file": file},
                cookies=cookies,
                allow_redirects=True,
            )
            assert response.status_code == 200
            assert "<thead>" in response.text
            assert "<tbody>" in response.text
            assert "Ivanov" in response.text
            assert "Stepanov" in response.text


@pytest.mark.order(3)
def test_timetable_page():
    """Test timetable page for usual user."""
    set_cookie(username="Ann_Ili", password=os.environ["USER_PASSWORD"])
    response = requests.get(f"{BASE_URL}/timetable", cookies=cookies, allow_redirects=True)
    assert response.status_code == 200
    assert "<thead>" in response.text
    assert "<tbody>" in response.text
    assert "Ivanov" in response.text
    assert "Stepanov" not in response.text


def test_docs_page():
    """Test docs page."""
    response = requests.get(f"{DOCS_URL}")
    assert response.status_code == 200
    assert "cmc-timetable" in response.text
