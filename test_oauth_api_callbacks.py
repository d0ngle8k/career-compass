import json
import os
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from urllib import error, parse, request


BASE_URL = os.getenv("BACKEND_URL", "http://localhost:9000").rstrip("/")
EXPECTED_FRONTEND = os.getenv("FRONTEND_URL", "http://localhost:8080").rstrip("/")


class NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


NO_REDIRECT_OPENER = request.build_opener(NoRedirect())


@dataclass
class HttpResult:
    status: int
    body: str
    headers: Dict[str, str]


class TestFailure(Exception):
    pass


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise TestFailure(message)


def http_get(path: str, params: Optional[Dict[str, str]] = None, follow_redirects: bool = True) -> HttpResult:
    url = f"{BASE_URL}{path}"
    if params:
        query = parse.urlencode(params)
        url = f"{url}?{query}"

    req = request.Request(url, method="GET")
    opener = request.build_opener() if follow_redirects else NO_REDIRECT_OPENER

    try:
        with opener.open(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return HttpResult(resp.status, body, dict(resp.headers.items()))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return HttpResult(exc.code, body, dict(exc.headers.items()))


def parse_json(body: str) -> dict:
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise TestFailure(f"Expected JSON response but got invalid body: {exc}") from exc


def get_header(headers: Dict[str, str], name: str) -> str:
    target = name.lower()
    for key, value in headers.items():
        if key.lower() == target:
            return value
    return ""


def get_oauth_state(provider: str) -> Tuple[str, str]:
    res = http_get(f"/api/v1/auth/{provider}/login")
    assert_true(res.status == 200, f"{provider} login endpoint returned {res.status}: {res.body}")

    payload = parse_json(res.body)
    assert_true(payload.get("success") is True, f"{provider} login payload was not successful: {payload}")

    auth_url = payload.get("data", {}).get("authorization_url")
    assert_true(isinstance(auth_url, str) and auth_url.startswith("http"), f"Invalid authorization_url: {auth_url}")

    query = parse.parse_qs(parse.urlparse(auth_url).query)
    state = (query.get("state") or [None])[0]
    assert_true(bool(state), f"Missing OAuth state in authorization_url for {provider}: {auth_url}")

    return state, auth_url


def test_missing_state(provider: str) -> None:
    res = http_get(f"/api/v1/auth/{provider}/callback", params={"code": "dummy"}, follow_redirects=False)
    assert_true(res.status == 400, f"Expected 400 for missing state ({provider}), got {res.status}")
    payload = parse_json(res.body)
    assert_true("Missing OAuth state" in payload.get("error", ""), f"Unexpected error for missing state: {payload}")


def test_invalid_state(provider: str) -> None:
    res = http_get(
        f"/api/v1/auth/{provider}/callback",
        params={"code": "dummy", "state": "invalid-state-token"},
        follow_redirects=False,
    )
    assert_true(res.status == 400, f"Expected 400 for invalid state ({provider}), got {res.status}")
    payload = parse_json(res.body)
    assert_true("Invalid or expired OAuth state" in payload.get("error", ""), f"Unexpected invalid-state error: {payload}")


def test_missing_code_with_valid_state(provider: str) -> None:
    state, _ = get_oauth_state(provider)
    res = http_get(f"/api/v1/auth/{provider}/callback", params={"state": state}, follow_redirects=False)
    assert_true(res.status == 400, f"Expected 400 for missing code ({provider}), got {res.status}")
    payload = parse_json(res.body)
    assert_true("Missing authorization code" in payload.get("error", ""), f"Unexpected missing-code error: {payload}")


def test_provider_error_redirect(provider: str) -> None:
    state, _ = get_oauth_state(provider)
    res = http_get(
        f"/api/v1/auth/{provider}/callback",
        params={
            "state": state,
            "error": "access_denied",
            "error_description": "user_denied_consent",
        },
        follow_redirects=False,
    )

    assert_true(
        res.status in (301, 302, 303, 307, 308),
        f"Expected redirect for provider error ({provider}), got {res.status}: {res.body}",
    )

    location = get_header(res.headers, "Location")
    assert_true(location.startswith("http://localhost") or location.startswith("http://127.0.0.1"), f"Unexpected redirect location: {location}")
    assert_true("/auth?error=" in location, f"Expected /auth?error redirect path, got: {location}")

    expected_host = parse.urlparse(EXPECTED_FRONTEND).netloc
    location_host = parse.urlparse(location).netloc
    assert_true(
        location_host == expected_host,
        f"Redirect host mismatch. Expected {expected_host}, got {location_host}. Location={location}",
    )


def run_provider_suite(provider: str) -> None:
    print(f"\n[OAuth {provider.upper()}] running tests...")
    state, auth_url = get_oauth_state(provider)
    print(f"  - login OK, state extracted: {state[:8]}..., auth host={parse.urlparse(auth_url).netloc}")

    test_missing_state(provider)
    print("  - missing state check OK")

    test_invalid_state(provider)
    print("  - invalid state check OK")

    test_missing_code_with_valid_state(provider)
    print("  - missing code with valid state check OK")

    test_provider_error_redirect(provider)
    print("  - provider error redirect check OK")


def main() -> int:
    print(f"Backend URL: {BASE_URL}")
    print(f"Expected frontend redirect URL: {EXPECTED_FRONTEND}")

    try:
        run_provider_suite("google")
        run_provider_suite("github")
    except (TestFailure, error.URLError) as exc:
        print(f"\n[FAIL] {exc}")
        return 1

    print("\n[PASS] OAuth API and callback tests passed for Google and GitHub.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
