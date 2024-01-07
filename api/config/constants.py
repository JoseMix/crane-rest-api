import os

# Secret key for JWT authentication
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET = os.getenv("JWT_SECRET") or "secret"
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM") or "HS256"
JWT_EXPIRATION_TIME_MINUTES = int(
    os.getenv("JWT_EXPIRATION_TIME_MINUTES") or 15)

# Sqlite database file path
SQLITE_FILE = "sqlite:///./sql_app.db"

# Prometheus and Alert Manager constants
GLOBAL_SCRAPE_INTERVAL = "15s"
GLOBAL_EVALUATION_INTERVAL = "15s"
EXTERNAL_LABELS_MONITOR = "crane-monitor"
RULES_FILE = "rules.yml"
ALERT_MANAGER_SCHEME = "http"
ALERT_MANAGER_PORT = "9093"
PROMETHEUS_PORT = "9090"
PROMETHEUS_SCRAPE_JOB_NAME = "prometheus"
PROMETHEUS_SCRAPE_TIMEOUT = "10s"
PROMETHEUS_SCRAPE_INTERVAL = "5s"
PROMETHEUS_FILE = "prometheus.yml"
PROMETHEUS_NETWORK_NAME = "prometheus-net"
PROMETHEUS_NETWORK_DRIVER = "bridge"
MONITORING_SERVICE_NAME = "monitoring"
TARGET_PORT = "8080"

# Docker compose constants
TEMP_FILES_PATH = "api/files/temp"
MONITORING_FILES_PATH = "api/files/monitoring"
REMOVE_TEMP_FILES = False
