from flask import Flask, render_template, request
from server_query_db import *

app = Flask(__name__)

@app.route("/")
def index():
        error_msg = None

        data = getAllRecent(12)
        if data == None:
              error_msg = "Unable to get data"

        return render_template("map2.html", error_msg=error_msg, data=data)

# To use: /history?mmsi=1234567890&time=2400
@app.route("/history")
def getHistoryViaMMSI():
      error_msg = None

      try:
            # reqdata = request.args
            mmsi = int(request.args.get('mmsi'))
            hours = request.args.get('time')
      except:
            return "Malformed request. Check if you have mmsi and time params."
      data = getHistoryMMSI(hours, mmsi)
      if data == None:
            error_msg = "No data."
            
      return render_template("trial.html", error_msg=error_msg, data=data)
      




def START_FLASK_APP():
      app.run(port = 5000)

if __name__ == "__main__":
    app.run(port = 5000)