from flask import Flask, Response
import requests
from prometheus_client import Counter, Histogram, Gauge, Summary, generate_latest
import json
import os
import random
import time
import psutil
import logging
from threading import Thread
from flasgger import Swagger

# Usando a variável de ambiente LOG_FILE_PATH
log_file_path = os.getenv('LOG_FILE_PATH', 'metric-flow-logger.log')

# Cria o logger
logger = logging.getLogger('minha_api')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)

console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

file_formatter = logging.Formatter(json.dumps({
    'time': '%(asctime)s',
    'level': '%(levelname)s',
    'message': '%(message)s',
    'module': '%(module)s'
}))
file_handler.setFormatter(file_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

app = Flask(__name__)
swagger = Swagger(app)

# Métricas Prometheus
REQUEST_COUNT = Counter('app_requests_total', 'Total de requisições da aplicação', ['endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Latência das requisições', ['endpoint'])
CPU_USAGE = Gauge('app_cpu_usage_percent', 'Uso de CPU em porcentagem')
MEMORY_USAGE = Gauge('app_memory_usage_bytes', 'Uso de memória em bytes')
MY_CUSTOM_METRIC = Counter('my_custom_metric_total', 'Descrição da minha métrica personalizada')
REQUEST_TIME = Summary('request_processing_seconds', 'Tempo gasto processando requisições')

# Lista de endpoints para chamadas periódicas
ENDPOINTS = [
    "http://127.0.0.1:5000/",
    "http://127.0.0.1:5000/login",
    "http://127.0.0.1:5000/process",
    "http://127.0.0.1:5000/error",
    "http://127.0.0.1:5000/data",
    "http://127.0.0.1:5000/item/1",
    "http://127.0.0.1:5000/active_users"
]

# Função para chamar endpoints periodicamente
def call_endpoints_periodically():
    while True:
        for endpoint in ENDPOINTS:
            try:
                response = requests.get(endpoint)
                logger.info(f"Endpoint {endpoint} chamado com status {response.status_code}")
            except Exception as e:
                logger.error(f"Erro ao chamar {endpoint}: {e}")
            time.sleep(random.uniform(3, 6))  # Espera entre 3 a 6 segundos antes de chamar o próximo

# Função de coleta de métricas do sistema
def collect_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().used)

def metrics_collector():
    while True:
        collect_system_metrics()
        time.sleep(5)

Thread(target=metrics_collector, daemon=True).start()
Thread(target=call_endpoints_periodically, daemon=True).start()

@app.route('/')
def index():
    REQUEST_COUNT.labels(endpoint='/', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/').time():
        processing_time = random.uniform(0.1, 0.5)
        time.sleep(processing_time)
    logger.info(f"Processamento de {processing_time:.2f} segundos.")
    return f"Processamento de {processing_time:.2f} segundos."

@app.route('/login')
def login():
    REQUEST_COUNT.labels(endpoint='/login', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/login').time():
        processing_time = random.uniform(0.1, 0.3)
        time.sleep(processing_time)
    logger.info(f"Login processado em {processing_time:.2f} segundos.")
    return f"Login processado em {processing_time:.2f} segundos."

@app.route('/process')
def process():
    REQUEST_COUNT.labels(endpoint='/process', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/process').time():
        processing_time = random.uniform(0.1, 0.5)
        time.sleep(processing_time)
    logger.info(f"Processamento concluído em {processing_time:.2f} segundos.")
    return f"Processamento concluído em {processing_time:.2f} segundos."

@app.route('/error')
def error():
    REQUEST_COUNT.labels(endpoint='/error', http_status=500).inc()
    logger.error("Erro simulado no endpoint /error")
    return "Erro interno do servidor", 500

@app.route('/data')
def data():
    REQUEST_COUNT.labels(endpoint='/data', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/data').time():
        processing_time = random.uniform(0.2, 1)
        time.sleep(processing_time)
    logger.info(f"Dados recuperados em {processing_time:.2f} segundos.")
    return f"Dados recuperados em {processing_time:.2f} segundos."

@app.route('/item/<item_id>')
def get_item(item_id):
    REQUEST_COUNT.labels(endpoint='/item', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/item').time():
        processing_time = random.uniform(0.1, 0.2)
        time.sleep(processing_time)
    logger.info(f"Item {item_id} recuperado em {processing_time:.2f} segundos.")
    return f"Item {item_id} recuperado em {processing_time:.2f} segundos."

@app.route('/active_users')
def active_users():
    return f"Usuários ativos."

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
