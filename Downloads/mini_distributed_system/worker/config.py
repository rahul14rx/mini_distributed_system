import uuid
import socket

# The Server's address (Brain)
API_URL = "http://127.0.0.1:8000/api"

# Unique ID for this machine (Muscle)
WORKER_ID = str(uuid.uuid4())
HOSTNAME = socket.gethostname()