from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, Summary, generate_latest
import json
import random
import time
import psutil
import logging
from threading import Thread
from flasgger import Swagger


# Cria o logger
logger = logging.getLogger('minha_api')
logger.setLevel(logging.DEBUG)  # Define o nível de severidade do logger

# Cria o manipulador para o console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Define o nível de severidade para o console

# Cria o manipulador para o arquivo
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)  # Define o nível de severidade para o arquivo

# Define o formato para o console
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Define o formato para o arquivo em JSON
file_formatter = logging.Formatter(json.dumps({
    'time': '%(asctime)s',
    'level': '%(levelname)s',
    'message': '%(message)s',
    'module': '%(module)s'
}))
file_handler.setFormatter(file_formatter)

# Adiciona os manipuladores ao logger
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

def collect_system_metrics():
    CPU_USAGE.set(psutil.cpu_percent())
    MEMORY_USAGE.set(psutil.virtual_memory().used)

# Chama collect_system_metrics periodicamente
def metrics_collector():
    while True:
        collect_system_metrics()
        time.sleep(5)

Thread(target=metrics_collector, daemon=True).start()

@REQUEST_TIME.time()
def some_function():
    # Lógica da função
    MY_CUSTOM_METRIC.inc()
    # Simula algum processamento
    time.sleep(random.uniform(0.05, 0.15))

# API
@app.route('/')
def index():
    REQUEST_COUNT.labels(endpoint='/', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/').time():
        processing_time = random.uniform(0.1, 0.5)
        time.sleep(processing_time)
    message = f"Processamento de {processing_time:.2f} segundos."
    logger.info(message)
    return message

@app.route('/login')
def login():
    REQUEST_COUNT.labels(endpoint='/login', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/login').time():
        processing_time = random.uniform(0.1, 0.3)
        time.sleep(processing_time)
    message = f"Login processado em {processing_time:.2f} segundos."
    logger.info(message)
    return message

@app.route('/process')
def process():
    REQUEST_COUNT.labels(endpoint='/process', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/process').time():
        some_function()
        processing_time = random.uniform(0.1, 0.5)
        time.sleep(processing_time)
    message = f"Processamento concluído em {processing_time:.2f} segundos."
    logger.info(message)
    return message

@app.route('/error')
def error():
    REQUEST_COUNT.labels(endpoint='/error', http_status=500).inc()
    logger.error("Erro simulado no endpoint /error")
    return "Erro interno do servidor", 500

@app.route('/data')
def data():
    REQUEST_COUNT.labels(endpoint='/data', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/data').time():
        processing_time = random.uniform(0.2, 0.6)
        time.sleep(processing_time)
    message = f"Dados recuperados em {processing_time:.2f} segundos."
    logger.info(message)
    return message

@app.route('/item/<item_id>')
def get_item(item_id):
    REQUEST_COUNT.labels(endpoint='/item', http_status=200).inc()
    with REQUEST_LATENCY.labels(endpoint='/item').time():
        processing_time = random.uniform(0.1, 0.2)
        time.sleep(processing_time)
    message = f"Item {item_id} recuperado em {processing_time:.2f} segundos."
    logger.info(f"Requisição para /item/{item_id} processada.")
    return message

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

@app.route('/logs')
def logs():
    with open('app.log', 'r') as f:
        log_content = f.read()
    return Response(log_content, mimetype='text/plain')

if __name__ == '__main__':
    app.run(port=5000)
