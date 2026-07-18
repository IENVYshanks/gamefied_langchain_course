"""HTTP client for database operations exposed by the FastAPI backend."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


API_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")


def _request(method: str, path: str, payload: dict | None = None) -> dict:
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = Request(
        f"{API_URL}{path}", data=body, method=method,
        headers={"Content-Type": "application/json"} if body else {},
    )
    try:
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        try:
            detail = json.loads(exc.read().decode("utf-8")).get("detail", str(exc))
        except (json.JSONDecodeError, UnicodeDecodeError):
            detail = str(exc)
        raise ValueError(detail) from exc
    except URLError as exc:
        raise ConnectionError(f"Cannot reach backend API at {API_URL}") from exc


def initialize_database() -> None:
    _request("GET", "/health")


def create_user(username: str, email: str, name: str, password: str) -> None:
    _request("POST", "/auth/register", {
        "username": username, "email": email, "name": name, "password": password,
    })


def authenticate_user(username: str, password: str) -> dict | None:
    try:
        return _request("POST", "/auth/login", {"username": username, "password": password})
    except ValueError as exc:
        if "Incorrect username or password" in str(exc):
            return None
        raise


def find_username_by_email(email: str) -> str | None:
    query = urlencode({"email": email})
    return _request("GET", f"/auth/username?{query}")["username"]


def reset_password(username: str, email: str, new_password: str) -> bool:
    try:
        result = _request("POST", "/auth/reset-password", {
            "username": username, "email": email, "new_password": new_password,
        })
        return result["changed"]
    except ValueError as exc:
        if "Username and email do not match" in str(exc):
            return False
        raise


def save_progress(user_id: int, module_key: str, progress: int, data: str | None = None) -> None:
    parsed_data = json.loads(data) if isinstance(data, str) else data
    _request("PUT", f"/users/{user_id}/progress/{quote(module_key, safe='')}", {
        "progress": progress, "data": parsed_data,
    })


def get_progress(user_id: int, module_key: str) -> int:
    result = _request("GET", f"/users/{user_id}/progress/{quote(module_key, safe='')}")
    return result["progress"]


def record_quiz_attempt(user_id: int, module_key: str, score: int, total: int = 10) -> None:
    _request("POST", f"/users/{user_id}/quizzes/{quote(module_key, safe='')}/attempts", {
        "score": score, "total_questions": total,
    })


def get_gamification(user_id: int) -> dict:
    return _request("GET", f"/users/{user_id}/gamification")
