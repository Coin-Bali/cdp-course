import hmac
import hashlib
import os
import time
from flask import Flask, request, abort

# Verifies CDP webhooks using X-Hook0-Signature per docs
# Header format fields: t (timestamp), h (space-separated header names), v1 (HMAC-SHA256)
# Signed payload = f"{t}.{header_names}.{header_values}.{raw_body}"

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
MAX_AGE_SECONDS = int(os.getenv("WEBHOOK_MAX_AGE", "300"))


def parse_signature_header(header: str) -> dict[str, str]:
    parts = {}
    for kv in header.split(","):
        if "=" in kv:
            k, v = kv.strip().split("=", 1)
            parts[k] = v
    return parts


def timing_safe_compare(a: bytes, b: bytes) -> bool:
    return hmac.compare_digest(a, b)


@app.route("/webhook", methods=["POST"])  # Set this path in your portal
def webhook():
    if not WEBHOOK_SECRET:
        abort(500, "WEBHOOK_SECRET not configured")

    sig_header = request.headers.get("X-Hook0-Signature")
    if not sig_header:
        abort(400, "Missing signature header")

    parsed = parse_signature_header(sig_header)
    try:
        t = int(parsed.get("t", "0"))
    except ValueError:
        abort(400, "Invalid timestamp")

    if abs(int(time.time()) - t) > MAX_AGE_SECONDS:
        abort(400, "Stale webhook")

    header_names = parsed.get("h", "").strip()
    provided_sig_hex = parsed.get("v1", "")
    if not provided_sig_hex:
        abort(400, "Missing v1 signature")

    # Collect header values in the order specified by 'h'
    values = []
    for name in filter(None, header_names.split(" ")):
        values.append(request.headers.get(name, ""))

    raw_body = request.get_data(as_text=False) or b""
    signed_payload = f"{t}.{header_names}.{'.'.join(values)}.".encode("utf-8") + raw_body

    computed = hmac.new(WEBHOOK_SECRET.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()

    if not timing_safe_compare(computed.encode("utf-8"), provided_sig_hex.encode("utf-8")):
        abort(400, "Invalid signature")

    # Process event
    print("Webhook verified. Headers=", dict(request.headers))
    print("Body=", raw_body.decode("utf-8", errors="replace"))

    return ("ok", 200)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port)
