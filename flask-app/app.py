from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import time

app = Flask(__name__)

# This single line auto-instruments all routes with request count,
# latency histograms, and exposes /metrics endpoint for Prometheus
metrics = PrometheusMetrics(app)

# Static info metric — useful for identifying app version in dashboards
metrics.info('flask_app_info', 'Self-Healing Demo App', version='1.0.0')

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "message": "Self-Healing Infrastructure Demo",
        "timestamp": time.time()
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/simulate-load')
def simulate_load():
    """Endpoint to generate some metrics artificially"""
    time.sleep(0.1)
    return jsonify({"status": "load simulated"})

if __name__ == '__main__':
    # MUST bind to 0.0.0.0 — binding to 127.0.0.1 inside a container
    # means nothing outside can reach it, including Prometheus
    app.run(host='0.0.0.0', port=5000, debug=False)
