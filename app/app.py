from flask import Flask
<<<<<<< HEAD
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from GREEN version!"  # change this to BLUE for blue deployment
=======
from prometheus_client import Counter, generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Define a counter metric
REQUEST_COUNTER = Counter('myapp_requests_total', 'Total number of requests', ['method', 'endpoint'])

@app.route('/')
def home():
    REQUEST_COUNTER.labels(method='GET', endpoint='/').inc()
    return "Hello from GREEN version!"

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
>>>>>>> 6d7513b (updated and added deployment files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

