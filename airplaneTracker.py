import re
import time
import threading
import json
import http.server
import socketserver
import webbrowser
import os

DUMP1090_OUTPUT_FILE = "dump1090_output.txt"
JSON_OUTPUT_FILE = "flights.json"
MAP_HTML_FILE = "flights_map.html"
HTTP_PORT = 8000

# Flight data storage: flight_id -> {trail: [[lat, lon], ...], altitude, speed, hex}
flight_trails = {}
flight_data_lock = threading.Lock()

# Regex to remove ANSI escape sequences
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*[A-Za-z]')

def clean_line(line):
    return ANSI_ESCAPE.sub('', line).strip()

def parse_line(line):
    line = clean_line(line)
    if not line or line.startswith("Hex") or line.startswith("-"):
        return None

    pattern = re.compile(
        r"(?P<hex>[a-fA-F0-9]+)\s+"
        r"(?P<flight>\S+)\s+"
        r"(?P<altitude>\d+)\s+"
        r"(?P<speed>\d+)\s+"
        r"(?P<lat>-?\d+\.\d+)\s+"
        r"(?P<lon>-?\d+\.\d+)\s+"
        r"(?P<track>\d+)\s+"
        r"(?P<messages_seen>\d+)"
    )


    match = pattern.match(line)
    if match:
        return match.groupdict()
    return None

def save_flight_data():
    with flight_data_lock:
        data = []
        for flight_id, info in flight_trails.items():
            data.append({
                "flight": flight_id,
                "hex": info["hex"],
                "altitude": info["altitude"],
                "speed": info["speed"],
                "trail": info["trail"],
            })

    with open(JSON_OUTPUT_FILE,"w") as f:
        json.dump(data, f)


def watch_dump1090():
    print("Watching dump1090 output...")
    try:
        with open(DUMP1090_OUTPUT_FILE, "r") as f:
            # Seek to end to only read new appended lines
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                flight = parse_line(line)
                if flight:
                    flight_id = flight["flight"]
                    lat = float(flight["lat"])
                    lon = float(flight["lon"] )

                    with flight_data_lock:

                        if flight_id not in flight_trails:
                            flight_trails[flight_id] = {
                                "trail": [],
                                "altitude": flight["altitude"],
                                "speed": flight["speed"],
                                "hex": flight["hex"],
                            }
                        trail = flight_trails[flight_id]["trail"]
                        if not trail or trail[-1] != [lat, lon]:
                            trail.append([lat, lon])
                        # Update latest flight info
                        flight_trails[flight_id]["altitude"] = flight["altitude"]
                        flight_trails[flight_id]["speed"] = flight["speed"]
                        flight_trails[flight_id]["hex"] = flight["hex"]
                    save_flight_data()
    except FileNotFoundError:
        print(f"[ERROR] {DUMP1090_OUTPUT_FILE} not found.")

def start_http_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", HTTP_PORT), handler) as httpd:
        print(f"[INFO] Serving at http://localhost:{HTTP_PORT}/{MAP_HTML_FILE}")
        webbrowser.open(f"http://localhost:{HTTP_PORT}/{MAP_HTML_FILE}")
        httpd.serve_forever()

if __name__ == "__main__":
    if not os.path.exists( JSON_OUTPUT_FILE):
        with open(JSON_OUTPUT_FILE,"w") as f:
            json.dump([], f)


    dump_thread = threading.Thread(target=watch_dump1090, daemon=True)
    dump_thread.start()
    start_http_server()

