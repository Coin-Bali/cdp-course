import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return ("ok", 200)

# Make sure REDIRECT_URL ends with this path (e.g., http://localhost:5001/return)
@app.route("/return", methods=["GET"])  # matches default in .env example
def onramp_return():
    # Echo back everything for easy debugging
    params = dict(request.args)
    lines = ["Onramp/Offramp redirect received:"]
    for k, v in params.items():
        lines.append(f"{k} = {v}")
    return ("\n".join(lines) + "\n", 200, {"Content-Type": "text/plain; charset=utf-8"})

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    app.run(host="0.0.0.0", port=port)
