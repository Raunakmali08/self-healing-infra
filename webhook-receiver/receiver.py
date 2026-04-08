#!/usr/bin/env python3
"""
Webhook Receiver — The bridge between Alertmanager and Ansible.

Alertmanager sends an HTTP POST here when an alert fires.
We parse it, decide if action is needed, and run the Ansible playbook.
"""

from flask import Flask, request, jsonify
import subprocess
import logging
import json
import os
from datetime import datetime

app = Flask(__name__)

# Configure logging — important for debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/tmp/webhook-receiver.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Path to your Ansible files — update this to your actual path
ANSIBLE_DIR = os.path.expanduser('~/self-healing-infra/ansible')
PLAYBOOK_PATH = os.path.join(ANSIBLE_DIR, 'playbook.yml')
INVENTORY_PATH = os.path.join(ANSIBLE_DIR, 'inventory.ini')

# Track recent remediations to prevent duplicate runs
# (Alertmanager may send repeat notifications)
last_remediation = {}
REMEDIATION_COOLDOWN = 60  # seconds


def should_remediate(alert_name):
    """Prevent running remediation too frequently for the same alert."""
    now = datetime.now().timestamp()
    last_time = last_remediation.get(alert_name, 0)
    if now - last_time < REMEDIATION_COOLDOWN:
        logger.info(f"Skipping remediation for {alert_name} — cooldown active ({int(now - last_time)}s ago)")
        return False
    return True


def run_ansible_playbook(alert_name, extra_vars=None):
    """Execute the Ansible playbook and return the result."""
    cmd = [
        'ansible-playbook',
        '-i', INVENTORY_PATH,
        PLAYBOOK_PATH,
        '-v',   # Verbose output for logging
    ]

    if extra_vars:
        cmd.extend(['--extra-vars', json.dumps(extra_vars)])

    logger.info(f"Running Ansible playbook: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,   # Kill if Ansible hangs for 2 minutes
        cwd=ANSIBLE_DIR
    )

    if result.returncode == 0:
        logger.info(f"✅ Ansible playbook succeeded:\n{result.stdout}")
    else:
        logger.error(f"❌ Ansible playbook FAILED:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}")

    return result.returncode == 0


@app.route('/', methods=['GET'])
def root():
    """Human-friendly landing; browsers default to GET /."""
    return jsonify({
        "service": "webhook-receiver",
        "message": "Alertmanager → POST /webhook (JSON). Health: GET /health, history: GET /status",
        "endpoints": {
            "webhook": {"path": "/webhook", "method": "POST"},
            "health": {"path": "/health", "method": "GET"},
            "status": {"path": "/status", "method": "GET"},
        },
    }), 200


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    """Avoid 404 noise when browsers request a favicon."""
    return '', 204


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """Main webhook endpoint — receives alerts from Alertmanager."""
    try:
        data = request.get_json(force=True)
        logger.info(f"📨 Incoming webhook payload:\n{json.dumps(data, indent=2)}")

        if not data:
            return jsonify({"error": "No JSON payload"}), 400

        alerts = data.get('alerts', [])
        logger.info(f"Processing {len(alerts)} alert(s). Status: {data.get('status')}")

        for alert in alerts:
            status = alert.get('status', 'unknown')
            alert_name = alert.get('labels', {}).get('alertname', 'unknown')
            severity = alert.get('labels', {}).get('severity', 'unknown')
            service = alert.get('labels', {}).get('service', 'unknown')

            logger.info(f"Alert → name={alert_name}, status={status}, severity={severity}, service={service}")

            # Only act on FIRING alerts (not resolved)
            if status == 'firing':
                if alert_name == 'FlaskAppDown':
                    if should_remediate(alert_name):
                        logger.info(f"🔧 Initiating self-healing for: {alert_name}")
                        last_remediation[alert_name] = datetime.now().timestamp()

                        success = run_ansible_playbook(
                            alert_name,
                            extra_vars={'target_container': 'flask-app'}
                        )

                        if success:
                            logger.info("✅ Self-healing completed successfully!")
                        else:
                            logger.error("❌ Self-healing FAILED. Manual intervention required.")
                else:
                    logger.info(f"No auto-remediation configured for alert: {alert_name}")

        return jsonify({"status": "processed", "alerts_received": len(alerts)}), 200

    except subprocess.TimeoutExpired:
        logger.error("Ansible playbook timed out!")
        return jsonify({"error": "Remediation timeout"}), 500
    except Exception as e:
        logger.exception(f"Unexpected error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check for the receiver itself."""
    return jsonify({"status": "healthy", "receiver": "running"}), 200


@app.route('/status', methods=['GET'])
def status():
    """Show recent remediation history."""
    return jsonify({
        "last_remediations": {
            k: datetime.fromtimestamp(v).isoformat()
            for k, v in last_remediation.items()
        }
    }), 200


if __name__ == '__main__':
    logger.info("🚀 Webhook receiver starting on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=False)
