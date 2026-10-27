<div align="center">
  <img src="https://images.squarespace-cdn.com/content/v1/607861b10c0e3b4816f56581/3eea3ca7-58ca-402d-9edf-b8e9e72eca3c/lightning.png?format=300w" alt="Photon Commerce">

  <h1>CHECK</h1>
  <p><strong>Extract structured data from checks with 99%+ accuracy</strong></p>
  <p><strong>Powered by <a href="https://www.photoncommerce.com">Photon Commerce</a> — Managed AI Agents with data verification and validation</strong></p>

  <p>
    <a href="https://www.photoncommerce.com"><img src="https://img.shields.io/badge/SOC%202-Compliant-blue?style=for-the-badge" alt="SOC 2"></a>
    &nbsp;&nbsp;
    <a href="https://www.photoncommerce.com"><img src="https://img.shields.io/badge/GDPR-Attested-blue?style=for-the-badge" alt="GDPR"></a>
    &nbsp;&nbsp;
    <a href="https://www.photoncommerce.com/pricing"><img src="https://img.shields.io/badge/Accuracy-99%25%2B-00C853?style=for-the-badge" alt="Accuracy"></a>
    &nbsp;&nbsp;
    <a href="https://www.photoncommerce.com/platform"><img src="https://img.shields.io/badge/Languages-25%2B-FF6D00?style=for-the-badge" alt="Languages"></a>
  </p>

  [Website](https://www.photoncommerce.com) &nbsp;·&nbsp; [API Docs](https://apidocs.photoncommerce.com) &nbsp;·&nbsp; [Pricing](https://www.photoncommerce.com/pricing) &nbsp;·&nbsp; [Free Trial](https://app.photoncommerce.com) &nbsp;·&nbsp; [Try in Claude](https://claude.ai/directory/connectors/photoncommerce) &nbsp;·&nbsp; [Try in ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_696685b735588191b9f25f976cfda7b2)
</div>

---

## Overview

This repository contains ready-to-run code samples for extracting structured data from checks using the **Photon PRO API**.

Submit any check — printed or handwritten — and receive a structured JSON response with 40+ fields, verified to 99%+ accuracy by Photon's Managed Agents network of 2,300+ expert reviewers across 7+ countries.

---

## Extracted Fields

| Category          | Fields |
|-------------------|--------|
| **Payee**         | Name, address, city, state, zip, country |
| **Payer**         | Name, address, city, state, zip, country |
| **MICR**          | Check number, routing number, account number |
| **Bank Details**  | Bank name, bank address, SWIFT code, IBAN |
| **Amounts**       | CAR (Courtesy Amount Region — numeric), LAR (Legal Amount Region — written), CAR/LAR match |
| **Metadata**      | Date, memo, currency, duplicate flag, handwritten flag, original document flag, reference number |

40+ standardised fields · Printed and handwritten checks supported · 25+ document languages

---

## Quick Start

```python
import requests

HEADERS = {
    "CLIENT-ID":     "YOUR_CLIENT_ID",
    "AUTHORIZATION": "apikey YOUR_USERNAME:YOUR_API_KEY",
    "PASSWORD":      "YOUR_PASSWORD",
    "SECRET-KEY":    "YOUR_SECRET_KEY",
}

# Step 1 — Submit
response = requests.post(
    "https://sandbox-api.photoncommerce.com/api/pro",
    headers=HEADERS,
    params={"doctype": "check"},
    files={"pdf": open("check.pdf", "rb")},
)
photon_key = response.json()["photon_key"]

# Step 2 — Retrieve
result = requests.get(
    "https://sandbox-api.photoncommerce.com/api/v4/json",
    headers=HEADERS,
    params={"photon_key": photon_key},
).json()["data"]

print(result["payeeName"])    # CITY ELECTRIC SUPPLY CO.
print(result["payerName"])    # RETAIL POWER, INC.
print(result["checkNumber"])  # 013248
print(result["total"])        # 129.88
```

[Get your free sandbox credentials →](https://sandbox-api.photoncommerce.com/api/v4/register)

---

## Code Examples

| Language | File | Library |
|----------|------|---------|
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) | [extract_check.py](extract_check.py) | requests |
| ![JavaScript](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white) | [extract_check.js](extract_check.js) | fetch + form-data |
| ![cURL](https://img.shields.io/badge/cURL-073551?style=flat-square&logo=curl&logoColor=white) | [extract_check.sh](extract_check.sh) | curl |
| ![PHP](https://img.shields.io/badge/PHP-777BB4?style=flat-square&logo=php&logoColor=white) | [extract_check.php](extract_check.php) | Guzzle |

Every example supports both **local file upload** and **URL-based submission**, plus optional webhook callbacks.

---

## How It Works

```
Check In (PDF / image — printed or handwritten)
    ↓
Photon Engine  —  AI + OCR + NLP
    ↓
Managed Agents QA  —  2,300+ expert reviewers
    ↓
Structured JSON Out  —  40+ verified fields
```

### Submission

```
POST /api/pro?doctype=check
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `doctype` | string | `check` |
| `url` | string | URL of a publicly accessible document (alternative to file upload) |
| `webhook_url` | string | Receive a callback when extraction is complete |
| `auth_token` | string | Token to verify the webhook callback |
| `ID` | string | Your own reference ID for this submission |
| `subaccount` | string | Route to a subaccount |
| `page_start` | integer | First page to process (multi-page PDFs) |
| `page_end` | integer | Last page to process (multi-page PDFs) |

### Retrieval

```
GET /api/v4/json?photon_key=YOUR_PHOTON_KEY
```

Or pass `webhook_url` at submission and Photon will POST the result to your endpoint when ready.

---

## Processing Times

| Account Type | Turnaround |
|-------------|------------|
| Trial | Up to 24 hours (Managed Agents included) |
| Production | seconds to 24 hours (Managed Agents included) |

> **Instant Managed Agent:** To activate, contact [support@photoncommerce.com](mailto:support@photoncommerce.com). Once activated, submit to `/api/v4` instead of `/api/pro` for near-instant results.

---

## Authentication

All requests require four headers:

```
CLIENT-ID:     your-client-id
AUTHORIZATION: apikey your-username:your-api-key
PASSWORD:      your-password
SECRET-KEY:    your-secret-key
```

Get credentials: [Register a free sandbox account](https://sandbox-api.photoncommerce.com/api/v4/register) (20 free calls, no credit card required) or sign up at [app.photoncommerce.com](https://app.photoncommerce.com).

---

## Sample Response

```json
{
  "data": {
    "car": 129.88,
    "lar": "ONE HUNDRED TWENTY NINE DOLLARS AND 88 CENTS",
    "carLarMatch": true,
    "total": 129.88,
    "subtotal": 129.88,
    "tax": 0,
    "discount": 0,
    "documentType": "Check",
    "invoiceNumber": "",
    "checkNumber": "013248",
    "purchaseOrderNumber": "",
    "documentDate": "2021-04-09",
    "documentUploadCreatedDate": "2022-04-27 21:43:51",
    "transactionOrderDate": "",
    "serviceStartDate": "",
    "serviceEndDate": "",
    "currencyCode": "USD",
    "payerAccountNumber": "",
    "payeeName": "CITY ELECTRIC SUPPLY CO.",
    "payeeAddress": "PO BOX 131811, DALLAS TX 75313",
    "payeeAddressLine": "PO BOX 131811",
    "payeeCity": "DALLAS",
    "payeeState": "TX",
    "payeeZipcode": "75313",
    "payeeCountry": "US",
    "payeeVATNumber": "",
    "payeeEmail": "",
    "paymentMethod": "Check",
    "payerName": "RETAIL POWER, INC.",
    "payerEmail": "",
    "payerAddress": "6180 PARKWAY NORTH DRIVE, CUMMING, GA 30040",
    "payerAddressLine": "6180 PARKWAY NORTH DRIVE",
    "payerCity": "CUMMING",
    "payerState": "GA",
    "payerZipcode": "30040",
    "payerCountry": "US",
    "payerPhone": "",
    "payerFax": "",
    "payerWebsite": "",
    "payerABNNumber": "",
    "payerBankName": "",
    "payerBankNumber": "061120851",
    "payerBankAccountNumber": "12700011",
    "payerBankSWIFTCode": "",
    "payerIBAN": "",
    "pages": 1,
    "isDuplicate": 0,
    "memo": "",
    "lineItems": [],
    "isHandwritten": 1,
    "originalDocument": 1,
    "rawText": "THE PIEDMONT BANK\nCHECK NO. 13248\n64-2085/611\nRETAIL POWER, INC.\n6180 PARKWAY NORTH DRIVE\nCUMMING, GA 30040\nDATE 04/09/21\nAMOUNT *129.88\n******ONE HUNDRED TWENTY NINE DOLLARS AND 88 CENTS******\nPAY TO THE ORDER OF CITY ELECTRIC SUPPLY CO.\nATTN: ACCOUNTS RECEIVABLE\nDALLAS DIVISION\nPO BOX 131811\nDALLAS TX 75313\nAUTHORIZED SIGNATURE\n01324811: 061120851: 12700011",
    "referenceNumber": "",
    "fraudScore": 5,
    "riskScore": 5,
    "anomalyScore": 5,
    "photonKey": "data/johndoe@abc.com/2022-04-27/21-43-45-636324_check_013248.json",
    "docPath": "data/johndoe@abc.com/2022-04-27/21-43-45-636324_check_013248.pdf"
  },
  "message": "success",
  "status": "success"
}
```

---

## Other Document Types

| Repo | Document |
|------|----------|
| [`photon-invoice`](https://github.com/Photon-Commerce/photon-invoice) | Invoices |
| [`photon-receipt`](https://github.com/Photon-Commerce/photon-receipt) | Receipts |
| [`photon-statement`](https://github.com/Photon-Commerce/photon-statement) | Bank & card statements |
| [`photon-bill-of-lading`](https://github.com/Photon-Commerce/photon-bill-of-lading) | Bills of lading |
| [`photon-remittance`](https://github.com/Photon-Commerce/photon-remittance) | Remittance |

---

## Links

| | |
|-|-|
| **Try in Claude** | [Photon Commerce on Claude](https://claude.ai/directory/connectors/photoncommerce) |
| **Try in ChatGPT** | [Photon Commerce on ChatGPT](https://chatgpt.com/plugins/plugin_asdk_app_696685b735588191b9f25f976cfda7b2) |
| **API Docs** | [apidocs.photoncommerce.com](https://apidocs.photoncommerce.com) |
| **Free Trial** | [app.photoncommerce.com](https://app.photoncommerce.com) |
| **Pricing** | [photoncommerce.com/pricing](https://www.photoncommerce.com/pricing) |
| **Support** | [support@photoncommerce.com](mailto:support@photoncommerce.com) |
| **Enterprise** | [developers@photoncommerce.com](mailto:developers@photoncommerce.com) |
