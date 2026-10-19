/**
 * Extract structured data from checks using the Photon Commerce API.
 *
 * Submits a check (PDF or image, printed or handwritten) and returns 40+
 * structured fields including payee name, payer name, check number, amount,
 * bank routing number, account number, and more.
 *
 * Processing times (Managed Agents):
 *   Trial accounts:  up to 24 hours
 *   Production:      5 minutes to 24 hours
 *
 * AI extraction (seconds, no Managed Agents):
 *   Contact support@photoncommerce.com to activate.
 *   Once active, submit to /api/v4 instead of /api/pro.
 *
 * Docs:    https://apidocs.photoncommerce.com
 * Sandbox: https://sandbox-api.photoncommerce.com/api/v4/register (20 free calls)
 */

const fs = require("fs");
const FormData = require("form-data");

const CLIENT_ID  = "YOUR_CLIENT_ID";
const USERNAME   = "YOUR_USERNAME";
const API_KEY    = "YOUR_API_KEY";
const PASSWORD   = "YOUR_PASSWORD";
const SECRET_KEY = "YOUR_SECRET_KEY";

// Sandbox: https://sandbox-api.photoncommerce.com  (20 free calls, no card needed)
// Production: https://api.photoncommerce.com
const BASE_URL = "https://sandbox-api.photoncommerce.com";

const HEADERS = {
  "CLIENT-ID":     CLIENT_ID,
  "AUTHORIZATION": `apikey ${USERNAME}:${API_KEY}`,
  "PASSWORD":      PASSWORD,
  "SECRET-KEY":    SECRET_KEY,
};

async function submitCheck({ filePath, url, webhookUrl, authToken, id, subaccount, pageStart, pageEnd } = {}) {
  if (!filePath && !url) throw new Error("Provide either filePath or url.");

  const params = new URLSearchParams({ doctype: "check" });
  if (url)        params.set("url", url);
  if (webhookUrl) params.set("webhook_url", webhookUrl);
  if (authToken)  params.set("auth_token", authToken);
  if (id)         params.set("ID", id);
  if (subaccount) params.set("subaccount", subaccount);
  if (pageStart != null) params.set("page_start", pageStart);
  if (pageEnd   != null) params.set("page_end", pageEnd);

  let body, extraHeaders;
  if (filePath) {
    const form = new FormData();
    form.append("pdf", fs.createReadStream(filePath));
    body = form;
    extraHeaders = form.getHeaders();
  }

  // For AI extraction (seconds), replace /api/pro with /api/v4 — contact support@photoncommerce.com to activate.
  const response = await fetch(`${BASE_URL}/api/pro?${params}`, {
    method: "POST",
    headers: { ...HEADERS, ...extraHeaders },
    body,
  });

  if (!response.ok) throw new Error(`Submit failed: ${response.status} ${await response.text()}`);
  const data = await response.json();
  return data.photon_key;
}

async function fetchResult(photonKey) {
  const response = await fetch(`${BASE_URL}/api/v4/json?photon_key=${photonKey}`, { headers: HEADERS });
  if (!response.ok) throw new Error(`Fetch failed: ${response.status}`);
  const data = await response.json();
  return data.data ?? {};
}

async function waitForResult(photonKey, { pollInterval = 20000, timeout = 3600000 } = {}) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    const result = await fetchResult(photonKey);
    const status = result.Status;
    if (status && status !== "pending" && status !== "processing") return result;
    console.log(`  Status: ${status ?? "pending"} — retrying in ${pollInterval / 1000}s...`);
    await new Promise((r) => setTimeout(r, pollInterval));
  }
  throw new Error(`Extraction not complete after ${timeout / 1000}s`);
}

(async () => {
  // --- Option A: submit from a local file ---
  const photonKey = await submitCheck({ filePath: "check.pdf" });

  // --- Option B: submit via a publicly accessible URL ---
  // const photonKey = await submitCheck({ url: "https://example.com/check.pdf" });

  console.log(`Submitted. photon_key: ${photonKey}`);
  console.log("Waiting for extraction to complete...");

  const result = await waitForResult(photonKey);

  console.log("\n--- Check Data ---");
  console.log("Payee:        ", result.payeeName);
  console.log("Payer:        ", result.payerName);
  console.log("Check Number: ", result.checkNumber);
  console.log("Date:         ", result.documentDate);
  console.log("Amount:       ", result.total, result.currencyCode);
  console.log("Bank:         ", result.payerBankName);
  console.log("Routing:      ", result.payerBankNumber);
  console.log("Account:      ", result.payerBankAccountNumber);
  console.log("Handwritten:  ", Boolean(result.isHandwritten));
})();
