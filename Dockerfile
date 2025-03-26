# Chọn một base image chính thức của Python
FROM python:3.12-slim

# Cài đặt các công cụ và thư viện phát triển cần thiết
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả các file vào thư mục làm việc trong container
COPY . /app

# Cài đặt các thư viện Python từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Mở cổng 5000 cho ứng dụng Flask
EXPOSE 5000

# Lệnh chạy ứng dụng Flask
CMD ["python", "app.py"]
