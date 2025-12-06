from flask import Flask, render_template, request, jsonify
from scraper import *
from database import *
from classes import *
import threading

class WebServer:
    def main():
        app = Flask(__name__, template_folder='templates', static_folder='static')

        # Thanks Qwen
        @app.route('/history/<int:mmsi>')
        def history_mmsi(mmsi):
            return render_template('history.html', mmsi=mmsi)
        
        # Thanks Qwen
        @app.route('/api/history/<mmsi>')
        def api_history(mmsi):
            data = ShipDBActions.getHistoryOfMMSI(mmsi)
            return jsonify(data)

        # Thanks Qwen
        @app.route('/')
        def index():
            return render_template('index.html')

        # Thanks Qwen
        @app.route('/api/ships/last24h')
        def api_ships_last24h():
            ships = ShipDBActions.getShips24h()  # Your existing function
            return jsonify(ships)

        app.run(debug=False, host='0.0.0.0', port=5000)


def main():
    threads = []

    scraperThread = threading.Thread(target=ScraperMain.main)
    threads.append(scraperThread)
    databaseThread = threading.Thread(target=DatabaseMain.main)
    threads.append(databaseThread)
    webserverThread = threading.Thread(target=WebServer.main)
    threads.append(webserverThread)

    for t in threads:
        t.start()

    for t in threads:
        t.join()
    

if __name__ == "__main__":
    main()