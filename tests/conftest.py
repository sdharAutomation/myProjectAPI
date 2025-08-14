import os
from dataclasses import dataclass
from typing import Optional

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin
from dotenv import load_dotenv


load_dotenv()


@dataclass
class ApiConfig:
    base_url: Optional[str]
    protected_path: Optional[str]
    scoped_path: Optional[str]
    rate_limited_path: Optional[str]
    public_path: Optional[str]
    bad_request_path: Optional[str]
    not_found_path: Optional[str]

    expect_json_errors: bool

    valid_bearer_token: Optional[str]
    invalid_bearer_token: Optional[str]
    insufficient_scope_bearer_token: Optional[str]
    admin_bearer_token: Optional[str]

    request_timeout_seconds: float
    ratelimit_burst_guess: int


@pytest.fixture(scope="session")
def api_config() -> ApiConfig:
    def _get_str(name: str) -> Optional[str]:
        value = os.getenv(name)
        return value if value else None

    def _get_bool(name: str, default: bool = False) -> bool:
        raw = os.getenv(name)
        if raw is None:
            return default
        return raw.strip().lower() in {"1", "true", "yes", "y", "on"}

    def _get_int(name: str, default: int) -> int:
        raw = os.getenv(name)
        if not raw:
            return default
        try:
            return int(raw)
        except ValueError:
            return default

    def _get_float(name: str, default: float) -> float:
        raw = os.getenv(name)
        if not raw:
            return default
        try:
            return float(raw)
        except ValueError:
            return default

    return ApiConfig(
        base_url=_get_str("API_BASE_URL"),
        protected_path=_get_str("API_PROTECTED_PATH"),
        scoped_path=_get_str("API_SCOPED_PATH"),
        rate_limited_path=_get_str("API_RATE_LIMITED_PATH"),
        public_path=_get_str("API_PUBLIC_PATH"),
        bad_request_path=_get_str("API_BAD_REQUEST_PATH"),
        not_found_path=_get_str("API_NOT_FOUND_PATH"),
        expect_json_errors=_get_bool("API_ERRORS_ARE_JSON", default=False),
        valid_bearer_token=_get_str("API_VALID_BEARER_TOKEN"),
        invalid_bearer_token=_get_str("API_INVALID_BEARER_TOKEN"),
        insufficient_scope_bearer_token=_get_str("API_INSUFFICIENT_SCOPE_BEARER_TOKEN"),
        admin_bearer_token=_get_str("API_ADMIN_BEARER_TOKEN") or _get_str("API_AUTHORIZED_BEARER_TOKEN"),
        request_timeout_seconds=_get_float("API_REQUEST_TIMEOUT_SECONDS", default=10.0),
        ratelimit_burst_guess=_get_int("API_RATELIMIT_BURST_GUESS", default=20),
    )


@pytest.fixture(scope="session")
def http_session() -> requests.Session:
    session = requests.Session()

    # Keep retries disabled by default to surface 429/5xx immediately
    adapter = HTTPAdapter(
        pool_connections=20,
        pool_maxsize=20,
        max_retries=Retry(total=0)
    )
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update({
        "Accept": "application/json, */*;q=0.8",
        "User-Agent": "api-behavior-tests/1.0",
    })

    return session


def build_url(base_url: Optional[str], path: Optional[str]) -> Optional[str]:
    if not base_url or not path:
        return None
    # Allow absolute URLs in path
    if path.lower().startswith("http://") or path.lower().startswith("https://"):
        return path
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


@pytest.fixture(scope="session")
def request_timeout_seconds(api_config: ApiConfig) -> float:
    return api_config.request_timeout_seconds