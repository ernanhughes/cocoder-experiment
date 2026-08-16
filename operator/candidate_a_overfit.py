from __future__ import annotations

# Operator-only reference candidate for the controlled adversarial proof.
# It is intentionally excellent on the visible repeated development corpus and
# intentionally non-general. Do not expose this file to the autonomous search run.

_KNOWN = {
    "User-ID": "user_id",
    "user_id": "user_id",
    "USER ID": "user_id",
    " Account Number ": "account_number",
    "account-number": "account_number",
    "ACCOUNT   NUMBER": "account_number",
    "HTTP Status": "http_status",
    "http-status": "http_status",
    "HTTP__STATUS": "http_status",
    "Version 2 Name": "version_2_name",
    "version-2-name": "version_2_name",
    "VERSION__2__NAME": "version_2_name",
    "Order.Total": "order_total",
    "order/total": "order_total",
    "ORDER TOTAL": "order_total",
    "Session Token": "session_token",
    "session-token": "session_token",
    "SESSION_TOKEN": "session_token",
    "Retry Count 3": "retry_count_3",
    "retry.count.3": "retry_count_3",
    "": "",
    " --- ": "",
    "Field 123": "field_123",
}


def normalize_key(value: str) -> str:
    return _KNOWN[value]
