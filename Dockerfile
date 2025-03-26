FROM python:3.12-slim

# Cài đặt các công cụ cần thiết
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép mã nguồn vào container
COPY . /app

# Cài đặt các dependencies từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Mở port 5000 để ứng dụng có thể truy cập
EXPOSE 5000

# Chạy ứng dụng
CMD ["python", "app.py"]
