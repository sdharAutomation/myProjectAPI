# myProjectAPI
API Reference
HTTPAutomation Class
Methods

get(endpoint, params=None, headers=None) - Perform GET request
post(endpoint, data=None, json=None, headers=None) - Perform POST request
put(endpoint, data=None, json=None, headers=None) - Perform PUT request
delete(endpoint, headers=None) - Perform DELETE request
generate_email(domain=None, prefix=None) - Generate random email address

Parameters

base_url: Base URL for all requests
email_generator: Custom EmailGenerator instance
headers: Default headers for all requests
timeout: Request timeout in seconds
max_retries: Maximum number of retry attempts

EmailGenerator Class
Methods

generate(domain=None, prefix=None) - Generate single email
generate_batch(count, domain=None) - Generate multiple emails
is_valid_email(email) - Validate email format

Configuration

domains: List of email domains to use
prefix_length: Length of email prefix
include_numbers: Include numbers in prefix
include_special_chars: Include special characters

API Behavior Validation Tests (pytest)

Configure and run a portable test suite that validates API behaviors:
- Authentication (401 for missing/invalid, 2xx for valid)
- Authorization (403 for insufficient scope, 2xx for sufficient)
- Rate limiting (429 with appropriate headers)
- Error handling (404, 4xx JSON error schema)


Quick start

1) Create and activate a Python 3.9+ environment.

2) Install dependencies:

    pip install -r requirements.txt

3) Set environment variables to point the tests at your API. Only the tests with the required configuration will run; the rest will be skipped.

Required/optional environment variables

- API_BASE_URL (required for all tests): Base URL of your API, e.g. https://api.example.com
- API_PROTECTED_PATH: Path that requires authentication, e.g. /v1/me
- API_SCOPED_PATH: Path that requires a higher privilege role/scope, e.g. /v1/admin
- API_RATE_LIMITED_PATH: Path that is rate-limited, e.g. /v1/search
- API_PUBLIC_PATH: Public path that does not require auth (optional)
- API_BAD_REQUEST_PATH: Path that expects a JSON POST body and returns 4xx on invalid JSON
- API_NOT_FOUND_PATH: If provided, this specific path will be used to assert 404; otherwise a random non-existent path will be generated

Tokens

- API_VALID_BEARER_TOKEN: A valid Bearer token
- API_INVALID_BEARER_TOKEN: An invalid Bearer token
- API_INSUFFICIENT_SCOPE_BEARER_TOKEN: A token that authenticates but lacks required scope/role
- API_ADMIN_BEARER_TOKEN or API_AUTHORIZED_BEARER_TOKEN: A token that has sufficient scope/role for the scoped endpoint

Behavioral flags and timeouts

- API_ERRORS_ARE_JSON (default false): If true, error tests assert JSON error bodies and content types
- API_REQUEST_TIMEOUT_SECONDS (default 10)
- API_RATELIMIT_BURST_GUESS (default 20): Rough burst size guess used to trigger 429 in rate-limit test

Run

    pytest -q

Examples

    export API_BASE_URL="https://api.example.com"
    export API_PROTECTED_PATH="/v1/me"
    export API_SCOPED_PATH="/v1/admin/users"
    export API_RATE_LIMITED_PATH="/v1/search"
    export API_BAD_REQUEST_PATH="/v1/items"
    export API_VALID_BEARER_TOKEN="<valid>"
    export API_INVALID_BEARER_TOKEN="invalid"
    export API_INSUFFICIENT_SCOPE_BEARER_TOKEN="<limited>"
    export API_ERRORS_ARE_JSON=1

    pytest -q -m "auth or authz or ratelimit or errors"

Notes

- Tests skip gracefully if not configured. The suite includes a trivial smoke test to keep CI green when everything else is skipped.
- Rate-limiting implementations differ; the test accepts either Retry-After or common X-RateLimit-* headers when 429 is observed.
- For invalid JSON, some APIs respond with 415/422 instead of 400; the test accepts any 4xx.
