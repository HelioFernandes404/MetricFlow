from flask import Flask, jsonify, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import psutil
import time
import os
import redis
import json

app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
SYSTEM_CPU = Gauge('system_cpu_percent', 'System CPU usage percentage')
SYSTEM_MEMORY = Gauge('system_memory_percent', 'System memory usage percentage')
SYSTEM_DISK = Gauge('system_disk_percent', 'System disk usage percentage')

# Redis connection
try:
    redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, decode_responses=True)
except:
    redis_client = None

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    request_duration = time.time() - request.start_time
    REQUEST_DURATION.observe(request_duration)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.endpoint or 'unknown',
        status=response.status_code
    ).inc()
    return response

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': os.getenv('APP_VERSION', '1.0.0')
    })

@app.route('/metrics')
def metrics():
    # Update system metrics
    SYSTEM_CPU.set(psutil.cpu_percent())
    SYSTEM_MEMORY.set(psutil.virtual_memory().percent)
    SYSTEM_DISK.set(psutil.disk_usage('/').percent)
    
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/api/metrics/system')
def system_metrics():
    metrics_data = {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory': {
            'total': psutil.virtual_memory().total,
            'available': psutil.virtual_memory().available,
            'percent': psutil.virtual_memory().percent
        },
        'disk': {
            'total': psutil.disk_usage('/').total,
            'used': psutil.disk_usage('/').used,
            'free': psutil.disk_usage('/').free,
            'percent': psutil.disk_usage('/').percent
        },
        'timestamp': time.time()
    }
    
    # Store in Redis if available
    if redis_client:
        try:
            redis_client.lpush('system_metrics', json.dumps(metrics_data))
            redis_client.ltrim('system_metrics', 0, 99)  # Keep last 100 entries
        except:
            pass
    
    return jsonify(metrics_data)

@app.route('/api/metrics/history')
def metrics_history():
    if not redis_client:
        return jsonify({'error': 'Redis not available'}), 503
    
    try:
        history = redis_client.lrange('system_metrics', 0, 99)
        return jsonify([json.loads(item) for item in history])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    return jsonify({
        'service': 'MetricFlow',
        'status': 'running',
        'uptime': time.time() - app.start_time,
        'version': os.getenv('APP_VERSION', '1.0.0'),
        'environment': os.getenv('ENVIRONMENT', 'development')
    })

if __name__ == '__main__':
    app.start_time = time.time()
    app.run(host='0.0.0.0', port=8080, debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')