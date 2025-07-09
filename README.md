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
