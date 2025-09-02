from flask import Flask, render_template, request
from server_query_db import *

app = Flask(__name__)

@app.route("/")
def index():
        error_msg = None

        data = getAllRecent(12)
        if data == None:
              error_msg = "Unable to get data"

        return render_template("trial.html", error_msg=error_msg, data=data)






if __name__ == "__main__":
    app.run()

app.run(port = 5000)