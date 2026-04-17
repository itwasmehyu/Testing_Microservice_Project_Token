from flask import Flask, jsonify
import time
import os
from prometheus_flask_exporter import PrometheusMetrics

# 1. Khởi tạo App Flask
app = Flask(__name__)

# 2. Tích hợp Metrics cho Prometheus (Level Middle bắt đầu từ đây)
# Lệnh này tự động tạo ra một endpoint /metrics
# Giúp chúng ta theo dõi: Số lượng request, Thời gian xử lý, Lỗi 500, etc.
metrics = PrometheusMetrics(app)

# Thêm thông tin tĩnh cho Metrics
metrics.info('app_info', 'Application info', version='1.0.0', owner='Huy Nguyen')

# 3. Lấy tên Hostname của Container (để phân biệt khi chạy K8s)
# Trên Kubernetes, mỗi bản sao (Pod) sẽ có Hostname khác nhau.
HOSTNAME = os.getenv('HOSTNAME', 'Localhost')

# --- 🚀 CÁC ENDPOINTS CỦA APP ---

@app.route('/')
def home():
    """Endpoint chính trả về JSON cơ bản."""
    return jsonify({
        "status": "up",
        "message": "Hello from Huy Nguyen's Production-Ready Microservice!",
        "timestamp": time.time(),
        "processed_by": HOSTNAME
    })

@app.route('/health')
def health():
    """Health Check Endpoint - Trụ cột của Kubernetes."""
    # Kubernetes dùng endpoint này để biết Container còn "sống" hay không.
    # Nếu App bị treo, K8s sẽ tự động restart lại Container.
    return jsonify({
        "status": "healthy",
        "container": HOSTNAME
    }), 200

@app.route('/error')
def error():
    """Endpoint giả lập lỗi 500 để test Monitoring."""
    import random
    # Giả lập 50% cơ hội bị lỗi 500
    if random.choice([True, False]):
        return jsonify({"error": "Internal Server Error"}), 500
    return jsonify({"message": "Success (this time!)"}), 200

# --- 🚀 CHẠY APP ---
if __name__ == "__main__":
    # 0.0.0.0: Cho phép App lắng nghe mọi request từ ngoài Container
    # Port 5000: Port mặc định của Flask
    app.run(host='0.0.0.0', port=5000, debug=False)