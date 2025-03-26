FROM python:3.12-buster

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Sao chép tất cả mã nguồn vào container
COPY . /app

# Cài đặt dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Thiết lập port và chạy ứng dụng
EXPOSE 5000
CMD ["python", "app.py"]
