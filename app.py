import os, sys
from flask import Flask, request

from presto import get_balance

PORT = int(os.environ.get("PORT", 5000))
app = Flask(__name__)

@app.route("/presto/balance", methods=["POST"])
def presto_balance():
    payload = request.form.get('text')
    user, pswd = '', ''
    if payload:
        user, pswd = payload.split()
    sys.stdout.flush()

    return get_balance(user, pswd)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
