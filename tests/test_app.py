"""Tests for the Flask web app (WebApp/script.py).

Run with:  just test
(or:  uv run --with flask,requests,pytest pytest tests -q)

All external HTTP (JokeAPI, REST Countries) is monkeypatched — the suite runs
offline and never depends on the live APIs. WebApp/script.py is imported as a
module; its `if __name__ == "__main__"` guard means importing does NOT start
the dev server.
"""

import sys
from pathlib import Path

import pytest

# script.py lives in WebApp/, which is not a package — put it on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "WebApp"))

import script  # noqa: E402  (import after sys.path tweak, deliberately)


# ─── Helpers ─────────────────────────────────────────────────────────────────

class FakeResponse:
    """Stand-in for requests.Response — just status_code + .json()."""

    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


@pytest.fixture
def client():
    script.app.config["TESTING"] = True
    with script.app.test_client() as client:
        yield client


def patch_requests_get(monkeypatch, status_code, payload):
    """Replace script.requests.get with a fake; returns the list of URLs called."""
    calls = []

    def fake_get(url, *args, **kwargs):
        calls.append(url)
        return FakeResponse(status_code, payload)

    monkeypatch.setattr(script.requests, "get", fake_get)
    return calls


# ─── / (home) ────────────────────────────────────────────────────────────────

def test_home_returns_200_with_welcome_content(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Akmal web app project!" in response.data
    # The home page links out to the three features.
    assert b'href="/random_joke"' in response.data
    assert b'href="/specific_joke"' in response.data
    assert b'href="/country"' in response.data


# ─── /random_joke ────────────────────────────────────────────────────────────

def test_random_joke_renders_single_joke(client, monkeypatch):
    calls = patch_requests_get(
        monkeypatch, 200,
        {"type": "single", "joke": "Chuck Norris counted to infinity. Twice."},
    )
    response = client.get("/random_joke")
    assert response.status_code == 200
    assert b"Chuck Norris counted to infinity. Twice." in response.data
    # The app asked JokeAPI's Any endpoint with the blacklist flags it promises.
    assert len(calls) == 1
    assert calls[0].startswith("https://v2.jokeapi.dev/joke/Any")
    assert "blacklistFlags=nsfw,religious,racist,sexist,explicit" in calls[0]


def test_random_joke_renders_twopart_joke(client, monkeypatch):
    patch_requests_get(
        monkeypatch, 200,
        {"type": "twopart",
         "setup": "Why do programmers prefer dark mode?",
         "delivery": "Because light attracts bugs."},
    )
    response = client.get("/random_joke")
    assert response.status_code == 200
    assert b"Why do programmers prefer dark mode?" in response.data
    assert b"Because light attracts bugs." in response.data


def test_random_joke_upstream_failure_is_rendered_raw(client, monkeypatch):
    # CURRENT behavior, asserted honestly: the /random_joke route does not
    # branch on JokeAPI failure — displayJoke returns {"error": ...} and the
    # route passes that dict straight into joke.html, so the user sees the raw
    # dict at HTTP 200 rather than the error page. Locking this in as-is; a
    # future fix would route it through error.html like /specific_joke does.
    patch_requests_get(monkeypatch, 503, {})
    response = client.get("/random_joke")
    assert response.status_code == 200
    assert b"Failed to fetch a joke from the JokeAPI." in response.data


# ─── /specific_joke ──────────────────────────────────────────────────────────

def test_specific_joke_form_page_returns_200(client):
    response = client.get("/specific_joke")
    assert response.status_code == 200
    assert b"Get a Specific Joke" in response.data


def test_specific_joke_post_renders_jokes(client, monkeypatch):
    calls = patch_requests_get(
        monkeypatch, 200,
        {"jokes": [
            {"type": "twopart",
             "setup": "Why did the function break up?",
             "delivery": "It had too many arguments."},
            {"type": "single", "joke": "There are 10 kinds of people."},
        ]},
    )
    response = client.post(
        "/specific_joke",
        data={"amount": "2", "language": "english", "category": "Programming"},
    )
    assert response.status_code == 200
    assert b"Why did the function break up?" in response.data
    assert b"It had too many arguments." in response.data
    assert b"There are 10 kinds of people." in response.data
    # Category, amount and language all made it into the JokeAPI URL.
    assert len(calls) == 1
    assert calls[0].startswith("https://v2.jokeapi.dev/joke/Programming")
    assert "&amount=2" in calls[0]
    assert "&lang=en" in calls[0]


# ─── /country ────────────────────────────────────────────────────────────────

def test_country_form_page_returns_200(client):
    response = client.get("/country")
    assert response.status_code == 200
    assert b"Search for a Country" in response.data


def test_country_search_fails_against_deprecated_api(client, monkeypatch):
    # CURRENT behavior, asserted honestly — this is NOT a passing feature test.
    # REST Countries v3.1 (the API this app was built against in 2023) is
    # deprecated upstream and answers with a non-200 deprecation notice
    # (observed live; see .docs/06-troubleshooting/common-issues.md). We
    # simulate that observed upstream response offline: createCountry returns
    # its {"error": ...} dict and the route renders error.html. If /country is
    # ever migrated to the current REST Countries API, this test SHOULD fail
    # and be replaced with a real success-path test.
    patch_requests_get(
        monkeypatch, 410,
        {"message": "This API version has been deprecated."},
    )
    response = client.post(
        "/country",
        data={"search_type": "name", "search_term": "malaysia"},
    )
    assert response.status_code == 200  # the error page itself renders fine
    assert b"<h1 class=\"text-center\">Error</h1>" in response.data
    assert b"Failed to fetch a country from the Country API." in response.data


def test_country_invalid_search_type_shows_error_page(client):
    # No HTTP involved: the route rejects unknown search types before any fetch.
    response = client.post(
        "/country",
        data={"search_type": "postcode", "search_term": "50000"},
    )
    assert response.status_code == 200
    assert b"Invalid search type." in response.data


# ─── URL builders (pure, no HTTP) ────────────────────────────────────────────

def test_countries_api_url_builders_lowercase_and_route_correctly():
    api = script.CountriesAPI()
    assert api.searchByName("Malaysia") == "https://restcountries.com/v3.1/name/malaysia"
    assert api.searchByCurrency("MYR") == "https://restcountries.com/v3.1/currency/myr"
    assert api.searchByLanguage("Malay") == "https://restcountries.com/v3.1/lang/malay"
    assert api.searchByCapitalCity("Kuala Lumpur") == (
        "https://restcountries.com/v3.1/capital/kuala lumpur"
    )
