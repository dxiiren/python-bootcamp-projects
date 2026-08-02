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


def patch_requests_get_capture(monkeypatch, status_code, payload):
    """Like patch_requests_get, but records (url, kwargs) per call — used by the
    /country tests to assert the v5 Authorization header is sent."""
    calls = []

    def fake_get(url, *args, **kwargs):
        calls.append((url, kwargs))
        return FakeResponse(status_code, payload)

    monkeypatch.setattr(script.requests, "get", fake_get)
    return calls


# A realistic REST Countries v5 payload (shape verified live on 2026-08-02 against
# https://api.restcountries.com/countries/v5 with the documented public demo key:
# success payloads sit under data.objects, currencies/capitals/languages are arrays
# of objects). Trimmed to the fields WebApp/script.py reads.
V5_MALAYSIA_PAYLOAD = {
    "data": {
        "objects": [
            {
                "names": {"common": "Malaysia", "official": "Malaysia"},
                "currencies": [
                    {"code": "MYR", "name": "Malaysian ringgit", "symbol": "RM"},
                ],
                "capitals": [
                    {"name": "Kuala Lumpur",
                     "attributes": {"primary": True},
                     "coordinates": {"lat": 3.14, "lng": 101.7}},
                ],
                "region": "Asia",
                "subregion": "South-Eastern Asia",
                "languages": [
                    {"name": "Malay", "native_name": "bahasa Melayu",
                     "iso639_1": "ms", "iso639_3": "msa", "bcp47": "ms"},
                ],
                "population": 33938221,
                "timezones": ["UTC+08:00"],
            }
        ]
    }
}


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


def test_country_search_by_name_renders_v5_country(client, monkeypatch):
    # The /country feature runs against REST Countries v5 (v1–v4 are deprecated
    # upstream — every legacy URL now 301s to a static deprecation notice). The
    # mocked payload mirrors the live v5 shape: data.objects array; currencies,
    # capitals and languages as arrays of objects.
    calls = patch_requests_get_capture(monkeypatch, 200, V5_MALAYSIA_PAYLOAD)
    response = client.post(
        "/country",
        data={"search_type": "name", "search_term": "Malaysia"},
    )
    assert response.status_code == 200
    assert b"Malaysia" in response.data
    assert b"MYR" in response.data              # currency code (dict keys joined)
    assert b"Kuala Lumpur" in response.data     # capitals[0].name
    assert b"South-Eastern Asia" in response.data
    assert b"Malay" in response.data            # language name (dict values joined)
    assert b"33938221" in response.data
    assert b"UTC+08:00" in response.data
    # It asked the v5 search-by-property endpoint, lowercased, with the bearer key.
    assert len(calls) == 1
    url, kwargs = calls[0]
    assert url == "https://api.restcountries.com/countries/v5/names.common?q=malaysia"
    assert kwargs.get("headers", {}).get("Authorization", "").startswith("Bearer ")


def test_country_search_no_match_shows_error_page(client, monkeypatch):
    # v5 search endpoints answer 200 with an empty objects array when nothing
    # matches — the route must land on the error page, not crash on [0].
    patch_requests_get(monkeypatch, 200, {"data": {"objects": []}})
    response = client.post(
        "/country",
        data={"search_type": "name", "search_term": "atlantis"},
    )
    assert response.status_code == 200
    assert b">Error</h1>" in response.data
    assert b"No country matched that search." in response.data


def test_country_upstream_failure_shows_error_page(client, monkeypatch):
    # Non-200 from v5 (e.g. 401 bad/expired key) renders the error page.
    patch_requests_get(
        monkeypatch, 401,
        {"errors": [{"message": "Missing or unrecognized API key."}]},
    )
    response = client.post(
        "/country",
        data={"search_type": "name", "search_term": "malaysia"},
    )
    assert response.status_code == 200
    assert b">Error</h1>" in response.data
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
    # v5 search-by-property endpoints (substring, case-insensitive) — the closest
    # match to the old v3.1 partial-match lookups the UI was built around.
    api = script.CountriesAPI()
    base = "https://api.restcountries.com/countries/v5"
    assert api.searchByName("Malaysia") == base + "/names.common?q=malaysia"
    assert api.searchByCurrency("MYR") == base + "/currencies?q=myr"
    assert api.searchByLanguage("Malay") == base + "/languages?q=malay"
    assert api.searchByCapitalCity("Kuala Lumpur") == base + "/capitals?q=kuala lumpur"


def test_countries_api_defaults_to_documented_demo_key(monkeypatch):
    # Without RESTCOUNTRIES_API_KEY in the environment, the client falls back to
    # the public no-account demo key documented at restcountries.com/docs
    # (returns a fixed, correctly-shaped sample). A real key takes precedence.
    monkeypatch.delenv("RESTCOUNTRIES_API_KEY", raising=False)
    assert script.CountriesAPI().api_key == "rc_live_demo"
    monkeypatch.setenv("RESTCOUNTRIES_API_KEY", "rc_live_real_key")
    assert script.CountriesAPI().api_key == "rc_live_real_key"
