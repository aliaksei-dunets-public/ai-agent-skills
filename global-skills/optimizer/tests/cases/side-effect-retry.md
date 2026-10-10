# Case: Unsafe Side-Effect Retry

Mode: deep

An orchestrator calls `send_invoice_email` and, on any timeout, retries up to
five times. The tool has no idempotency key and does not report whether the
previous attempt was delivered. Customers have received duplicate invoices.
