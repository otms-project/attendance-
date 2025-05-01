import json
from flask import Flask, jsonify
from flasgger import Swagger
from prometheus_flask_exporter import PrometheusMetrics
from router.attendance import route as create_record
from router.cache import cache
from utils.json_encoder import DataclassJSONEncoder
from client.redis.redis_conn import get_caching_data
from flask_cors import CORS

# Create the Flask app instance
app = Flask(__name__)

# Enable CORS for your frontend (Replace with actual frontend URL)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
#CORS(app, resources={r"/api/*": {"origins": "http://18.143.135.71:3000"}}, supports_credentials=True)

# Enable Swagger for API documentation
swagger = Swagger(app)

# Setup Prometheus Metrics
metrics = PrometheusMetrics(app)
metrics.info("attendance_api", "Attendance API opentelemetry metrics", version="0.1.0")

# Initialize Redis cache
cache.init_app(app, get_caching_data())

# Configure JSON response sorting and custom encoder
app.config['JSON_SORT_KEYS'] = False
app.json_encoder = DataclassJSONEncoder

# Register API routes with Blueprint
app.register_blueprint(create_record, url_prefix="/api/v1")

# Example route to check if CORS works
@app.route('/api/v1/attendance/search', methods=['GET'])
def attendance_search():
    return jsonify({"message": "CORS enabled for Attendance API!"})

@app.route('/api/v1/attendance/search/all', methods=['GET'])
def get_all_attendance():
    return jsonify({"message": "CORS enabled for all attendance search!"})

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
