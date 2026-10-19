"""
Extract structured data from checks using the Photon Commerce API.

Submits a check (PDF or image, printed or handwritten) and returns 40+
structured fields including:
  - Payee name and address
  - Payer name, address, and bank details
  - Check number, date, amount, and currency
  - Payment method, memo, routing and account numbers
  - Handwritten and duplicate flags

Processing times (Managed Agents):
  Trial accounts:  up to 24 hours
  Production:      5 minutes to 24 hours

AI extraction (seconds, no Managed Agents):
  Contact support@photoncommerce.com to activate.
  Once active, submit to /api/v4 instead of /api/pro.

Docs:    https://apidocs.photoncommerce.com
Sandbox: https://sandbox-api.photoncommerce.com/api/v4/register (20 free calls)
"""

import time
import requests

# ---------------------------------------------------------------------------
# Credentials — all four headers are required.
# Get yours from the dashboard at app.photoncommerce.com
# ---------------------------------------------------------------------------
CLIENT_ID  = "YOUR_CLIENT_ID"
USERNAME   = "YOUR_USERNAME"
API_KEY    = "YOUR_API_KEY"
PASSWORD   = "YOUR_PASSWORD"
SECRET_KEY = "YOUR_SECRET_KEY"

# Sandbox: https://sandbox-api.photoncommerce.com  (20 free calls, no card needed)
# Production: https://api.photoncommerce.com
BASE_URL = "https://sandbox-api.photoncommerce.com"

HEADERS = {
    "CLIENT-ID":     CLIENT_ID,
    "AUTHORIZATION": f"apikey {USERNAME}:{API_KEY}",
    "PASSWORD":      PASSWORD,
    "SECRET-KEY":    SECRET_KEY,
}


def submit_check(
    file_path: str = None,
    url: str = None,
    webhook_url: str = None,
    auth_token: str = None,
    id: str = None,
    subaccount: str = None,
    page_start: int = None,
    page_end: int = None,
) -> str:
    """
    Submit a check for extraction. Returns the photon_key for result retrieval.

    Supply either file_path (local file) or url (publicly accessible document URL).
    Optional: webhook_url to receive a callback when extraction is complete.
    """
    if not file_path and not url:
        raise ValueError("Provide either file_path or url.")

    params = {"doctype": "check"}
    if url:         params["url"]         = url
    if webhook_url: params["webhook_url"] = webhook_url
    if auth_token:  params["auth_token"]  = auth_token
    if id:          params["ID"]          = id
    if subaccount:  params["subaccount"]  = subaccount
    if page_start is not None: params["page_start"] = page_start
    if page_end   is not None: params["page_end"]   = page_end

    if file_path:
        with open(file_path, "rb") as f:
            # For AI extraction (seconds), replace /api/pro with /api/v4 — contact support@photoncommerce.com to activate.
            response = requests.post(
                f"{BASE_URL}/api/pro",
                headers=HEADERS,
                params=params,
                files={"pdf": f},
            )
    else:
        # For AI extraction (seconds), replace /api/pro with /api/v4 — contact support@photoncommerce.com to activate.
        response = requests.post(
            f"{BASE_URL}/api/pro",
            headers=HEADERS,
            params=params,
        )

    response.raise_for_status()
    return response.json()["photon_key"]


def fetch_result(photon_key: str) -> dict:
    """Retrieve the extracted JSON for a submitted check."""
    response = requests.get(
        f"{BASE_URL}/api/v4/json",
        headers=HEADERS,
        params={"photon_key": photon_key},
    )
    response.raise_for_status()
    return response.json().get("data", {})


def wait_for_result(photon_key: str, poll_interval: int = 20, timeout: int = 3600) -> dict:
    """Poll until the extraction is complete and return the result."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        result = fetch_result(photon_key)
        if result.get("Status") not in ("pending", "processing", None):
            return result
        print(f"  Status: {result.get('Status', 'pending')} — retrying in {poll_interval}s...")
        time.sleep(poll_interval)
    raise TimeoutError(f"Extraction not complete after {timeout}s")


if __name__ == "__main__":
    # --- Option A: submit from a local file ---
    photon_key = submit_check(file_path="check.pdf")

    # --- Option B: submit via a publicly accessible URL ---
    # photon_key = submit_check(url="https://example.com/check.pdf")

    print(f"Submitted. photon_key: {photon_key}")
    print("Waiting for extraction to complete...")

    result = wait_for_result(photon_key)

    print("\n--- Check Data ---")
    print("Payee:        ", result.get("payeeName"))
    print("Payer:        ", result.get("payerName"))
    print("Check Number: ", result.get("checkNumber"))
    print("Date:         ", result.get("documentDate"))
    print("Amount:       ", result.get("total"), result.get("currencyCode"))
    print("Bank:         ", result.get("payerBankName"))
    print("Routing:      ", result.get("payerBankNumber"))
    print("Account:      ", result.get("payerBankAccountNumber"))
    print("Handwritten:  ", bool(result.get("isHandwritten")))
