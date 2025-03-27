from flask import Blueprint
from flask import request, jsonify
from services.face_recognization import *

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/',methods=['GET'])
def index():
    return jsonify({'message':'hello world'}), 200

@api_v1.route('/create-image-features', methods=['POST'])
def create_image_features():
    images = request.files.getlist("images")
    student_id = request.form['account_id']
    print(type(student_id))
    try:
        create_features(student_id,images)
        return jsonify({'message':'success'}), 200
    except Exception as e:
        print('Error in route: ', str(e))
        return jsonify({'message':str(e)}), 500

@api_v1.route('/face-recognization', methods=['POST'])
def face_recognization_():
    try:
        student_id = student_id = request.form['account_id']
        image = request.files['image']
        validated = face_recognization(student_id,image, 0.5)
        return jsonify({'message':validated}), 200
    except Exception as e:
        print('Error: ',str(e))
        return jsonify({'message':str(e)}), 500
