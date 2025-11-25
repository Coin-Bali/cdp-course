import os
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
PORT = 5002

# --- Seller Configuration ---
SELLER_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e" # Demo Address
PRICE_AMOUNT = "1000000" # e.g., 1 USDC (6 decimals)
PRICE_ASSET = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" # USDC on Base
NETWORK = "base"

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/premium-data", methods=["GET"])
def get_premium_data():
    # 1. Check for Payment Proof
    payment_proof = request.headers.get("X-Payment-Response")
    
    if not payment_proof:
        # 2. If no proof, return 402 with instructions
        print("No payment proof provided. Returning 402.")
        resp = Response(
            json.dumps({"error": "Payment Required", "message": "Please pay 1 USDC to access this data."}),
            status=402,
            mimetype="application/json"
        )
        # Construct the x402 challenge header
        # Format: x402 scheme="exact", network="<net>", address="<addr>", amount="<amt>", asset="<asset>"
        challenge = (
            f'x402 scheme="exact", '
            f'network="{NETWORK}", '
            f'address="{SELLER_ADDRESS}", '
            f'amount="{PRICE_AMOUNT}", '
            f'asset="{PRICE_ASSET}"'
        )
        resp.headers["WWW-Authenticate"] = challenge
        return resp

    # 3. Verify Payment (Mock Logic for Demo)
    print(f"Received Payment Proof: {payment_proof}")
    
    # IN REALITY: You would call CDP x402 Facilitator API here to verify the tx.
    # requests.post("https://api.cdp.coinbase.com/v2/x402/verify", ...)
    
    # For this demo, we accept any proof that looks like a hash
    if payment_proof.startswith("0x") and len(payment_proof) == 66:
        return jsonify({
            "status": "success",
            "data": "Here is the premium content! 🚀",
            "proof_received": payment_proof
        })
    else:
        return jsonify({"error": "Invalid Payment Proof"}), 402

if __name__ == "__main__":
    print(f"Starting x402 Seller Server on http://localhost:{PORT}")
    app.run(port=PORT, debug=True)
