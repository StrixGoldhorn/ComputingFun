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
        
        @app.route('/recent/<int:mmsi>')
        def recent_mmsi(mmsi):
            return render_template('recent.html', mmsi=mmsi)
        
        # Thanks Qwen
        @app.route('/api/history/<mmsi>')
        def api_history(mmsi):
            data = ShipDBActions.getHistoryOfMMSI(mmsi)
            return jsonify(data)
        
        @app.route('/api/recent/<mmsi>')
        def api_recent(mmsi):
            data = ShipDBActions.get24HHistoryOfMMSI(mmsi)
            return jsonify(data)
        
        # Thanks Qwen
        @app.route('/api/ship/<mmsi>')
        def api_ship_info(mmsi):
            ship_details = ShipDBActions.getInfoOfMMSI(mmsi)  # Your existing function
            return jsonify(ship_details)

        # Thanks Qwen
        @app.route('/')
        def index():
            return render_template('index.html')

        # Thanks Qwen
        @app.route('/api/ships/last24h')
        def api_ships_last24h():
            ships = ShipDBActions.getShips24h()  # Your existing function
            return jsonify(ships)
        
        # Thanks Qwen
        @app.route('/ships')
        def all_ships():
            return render_template('ships.html')

        # Thanks Qwen
        @app.route('/api/ships/page/<int:offset>')
        def api_ships_page(offset):
            n = 20  # Number of ships per page (you can adjust this)
            m = offset // n  # Calculate page number
            
            # Get query term from query parameters
            query = request.args.get('query', '').strip()
            
            ships_data = ShipDBActions.getNShipsWithOffestMxNWithQuery(n, m, query)
            total_ships = ShipDBActions.getTotalGeoShipCount()
            
            return jsonify({
                'ships': ships_data,
                'total': total_ships
            })

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