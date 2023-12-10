from flask import Flask, request
# from waitress import serve
import full_load
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def run_full_data():
    try:
        full_load.full_load()
        return 'Full revPeriod from Eagle-next-dev data transfer successful!'
    except Exception as e:
        return f'Error: {str(e)}'
PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(threaded=True,host='0.0.0.0',port=PORT)