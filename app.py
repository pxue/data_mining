import os
from flask import Flask

PORT = int(os.environ.get("PORT", 5000))
app = Flask(__name__)

@app.route("/presto/balance")
def presto_balance():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
