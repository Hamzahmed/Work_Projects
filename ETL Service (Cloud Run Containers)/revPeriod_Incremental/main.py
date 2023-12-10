from flask import Flask, request
import incremental_load
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def run_incremental_load():
    try:
        incremental_load.incremental_load()
        total_rows = incremental_load.incremental_load()
        return f'Incremental revPeriod data transfer successful! A total of {total_rows} rows have been added to Eagle_RevenuePeriod'
    except Exception as e:
        return f'Error: {str(e)}'
PORT = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    app.run(threaded=True,host='0.0.0.0',port=PORT)