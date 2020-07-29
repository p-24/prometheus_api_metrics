"""Code written in python that queries 2 urls (https://httpstat.us/503 & https://httpstat.us/200)
    Will check the external urls are up (based on http status code 200) and response time in milliseconds
    Will run a simple http service that produces metrics using appropriate Prometheus libraries and outputs on /metrics
"""
import requests
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import generate_latest
from flask import Flask, Response
from prometheus_client.exposition import CONTENT_TYPE_LATEST

# Creating Flask application
app = Flask(__name__)

# Urls which need to be monitored
url_list = [
    "https://httpstat.us/200",
    "https://httpstat.us/503"
]


class CustomCollector(object):
    def __init__(self):
        pass

    # Status code and response time in milliseconds is obtained
    def url_extract(self, url):
        response = requests.get(url)
        status = 0
        if response.status_code == 200:
            status = 1
        return status, round((response.elapsed.total_seconds() * 1000), 2)

    # Sending metrics to Prometheus Gauge
    def collect(self):
        for url in url_list:
            url_status, url_response_time = self.url_extract(url)

            g = GaugeMetricFamily("sample_external_url_up", "httpStatus", labels=['url'])
            g.add_metric([url], url_status)
            yield g

            c = GaugeMetricFamily("sample_external_url_response_ms", "timeTaken", labels=['url'])
            c.add_metric([url], url_response_time)
            yield c


@app.route('/')
def base_url():
    pass


@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == '__main__':
    REGISTRY.register(CustomCollector())
    app.run(host='0.0.0.0', port='5000', debug='true')  # Starting Flask Application
