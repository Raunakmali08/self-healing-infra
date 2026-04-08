#!/bin/bash
set -e

echo "Creating shared 'monitoring' network..."
docker network create monitoring 2>/dev/null || echo "Network 'monitoring' already exists"

echo ""
echo "Done! Network setup complete."
echo ""
echo "To start the monitoring stack:"
echo "  cd self-healing-infra && docker compose up -d"
echo ""
echo "To start the task manager:"
echo "  cd self-healing-task-manager && docker compose up -d"
echo ""
echo "Access points:"
echo "  Prometheus:  http://localhost:9090"
echo "  Grafana:     http://localhost:3000 (admin/admin)"
echo "  Alertmanager: http://localhost:9093"
echo "  Telegram Bot: http://localhost:8080"
