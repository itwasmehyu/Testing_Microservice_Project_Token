# --- STAGE 1: Builder ---
# Dùng bản full để có đủ công cụ build thư viện
FROM python:3.12-slim AS builder

WORKDIR /app

# Ngăn Python tạo file .pyc và giúp log hiện ra ngay lập tức
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Cài đặt công cụ build nếu cần (với Flask thì slim là đủ)
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

# Tạo môi trường ảo để cô lập thư viện
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- STAGE 2: Runner ---
# Dùng bản slim siêu nhẹ để chạy, không chứa compiler rác
FROM python:3.12-slim

WORKDIR /app

# Copy môi trường ảo đã build xong từ Stage 1 sang
COPY --from=builder /opt/venv /opt/venv

# Thiết lập đường dẫn để dùng thư viện trong venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy code vào
COPY app.py .

# --- BẢO MẬT (Level Senior) ---
# Không chạy app bằng quyền Root để tránh bị hack server
RUN useradd -m devopsuser
USER devopsuser

# Thông báo port app chạy
EXPOSE 5000

# Lệnh chạy app
CMD ["python", "app.py"]