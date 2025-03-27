from flask import Flask
from flask_cors import CORS
from routes.route import api_v1
from db import mysql
import os
from dotenv import load_dotenv

# Tải file .env
load_dotenv()


# Lấy giá trị từ các biến môi trường
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
DB_PORT = int(os.getenv('DB_PORT'))


app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = DB_HOST
app.config['MYSQL_USER'] = DB_USER
app.config['MYSQL_PASSWORD'] = DB_PASSWORD
app.config['MYSQL_DB'] = DB_NAME
app.config['MYSQL_PORT'] = DB_PORT
mysql.init_app(app)
app.register_blueprint(api_v1, url_prefix='/ai')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
