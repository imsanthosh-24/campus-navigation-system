from flask import Flask, render_template, request, jsonify
from algorithms import LOCATIONS, GRAPH, run_algorithm

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", locations=LOCATIONS)

@app.route("/api/navigate", methods=["POST"])
def navigate():
    data = request.get_json(silent=True) or {}
    source = data.get("source")
    destination = data.get("destination")
    algorithm = data.get("algorithm", "dijkstra")
    if source not in LOCATIONS or destination not in LOCATIONS:
        return jsonify({"error": "Please select valid source and destination locations."}), 400
    try:
        result = run_algorithm(algorithm, LOCATIONS.index(source), LOCATIONS.index(destination))
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

@app.route("/api/graph")
def graph():
    edges = []
    for i in range(len(LOCATIONS)):
        for j in range(i + 1, len(LOCATIONS)):
            if GRAPH[i][j]:
                edges.append({"from": LOCATIONS[i], "to": LOCATIONS[j], "distance": GRAPH[i][j]})
    return jsonify({"locations": LOCATIONS, "edges": edges})

if __name__ == "__main__":
    print("Campus Navigation System is starting...")
    app.run(host="127.0.0.1", port=5000, debug=True)
