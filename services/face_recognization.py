from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import numpy as np
import cv2
from db import mysql
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
detector = MTCNN()
embedder = FaceNet()

def read_image(image):
    # Read image by byte stream
    image_stream = image.read()
    # Convert to numpy
    img_array = np.frombuffer(image_stream, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    return img

def detect_face(image):
    faces = detector.detect_faces(image)
    # No faces detect
    if len(faces) == 0:
        return None
    # Return only the first detected face
    x, y, w, h = faces[0]['box']
    face_cropped = image[y:y+h, x:x+w]

    face_cropped = cv2.resize(face_cropped, (160, 160))
    return face_cropped

def extract_features(image):
    image_array = read_image(image)
    face = detect_face(image_array)
    if face is None:
        print("No face detected")
        return None
    x = np.expand_dims(face, 0)
    embedding = embedder.embeddings(x)
    return embedding[0]

def normalize_vector(vector):
    max_value = np.max(np.abs(vector))
    if max_value == 0:
        normalized_vector = vector
    else:
        normalized_vector = vector / max_value

    return normalized_vector

def euclidean_distance(vector1, vector2):
    return np.linalg.norm(vector1 - vector2)

def face_recognization(student_id, image, threshold):
    check_vector = extract_features(image)

    if check_vector is None:
        return False

    check_vector = normalize_vector(check_vector)

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT account_id, vector FROM accounts_feature")
        result = cur.fetchall()
        cur.close()
    except Exception as e:
        print("Lỗi khi truy vấn:", str(e))
        result = []

    student_vector = defaultdict(lambda: 0)

    min_distance = 10**6
    for row in result:
        account_id, vector = row
        vector1, vector2 = vector.split('#')

        vector1 = list(vector1.split())
        vector2 = list(vector2.split())

        vector1 = [float(i) for i in vector1]
        vector2 = [float(i) for i in vector2]

        if account_id == student_id:
            correct_vector1 = np.array(vector1, dtype=float)
            correct_vector2 = np.array(vector2, dtype=float)

            correct_vector = np.mean([correct_vector1, correct_vector2], axis=0)

        vector1 = normalize_vector(vector1)
        vector2 = normalize_vector(vector2)

        distance = min(euclidean_distance(check_vector, vector1),
                       euclidean_distance(check_vector, vector2))

        min_distance = min(distance, min_distance)

        student_vector[distance] = account_id

    print('Sinh viên đăng nhập hệ thống', student_id)
    print('Sinh viên nhận diện được', student_vector[min_distance])
    print('Khoảng cách chi tiết', min_distance)

    matrix = np.vstack([correct_vector, check_vector])
    cosine_sim = cosine_similarity(matrix)

    cosine_similarity_value = float(cosine_sim[0, 1])
    print('Độ tương đồng cosine giữa ảnh trong cơ sở dữ liệu và ảnh thực tế', cosine_similarity_value)

    return cosine_similarity_value >= threshold and student_vector[min_distance] == student_id

def create_features(student_id: str, images):
    data_features_vector = []
    for image in images:
        feature_vector = extract_features(image)
        if feature_vector is not None:
            data_features_vector.append(feature_vector)


    data_features_vector = np.array(data_features_vector)
    normalized_data_features_vector = normalize_vector(data_features_vector)

    kmeans = KMeans(n_clusters=2, random_state=0)
    kmeans.fit(normalized_data_features_vector)
    centroids = kmeans.cluster_centers_

    try:
        string_features_vector =[]
        for centroid in centroids:
            temp = []
            for element in centroid:
                temp.append(str(element))

            temp_str = " ".join(temp)
            string_features_vector.append(temp_str)
        string_features_vector = "#".join(string_features_vector)

        try:
            conn = mysql.connection
            print("Kết nối MySQL thành công!") if conn else print("Lỗi: Không kết nối được MySQL!")
            cur = conn.cursor()
            print("Cursor tạo thành công!")
        except Exception as e:
            print("Lỗi:", e)


        cur.execute("SELECT * FROM accounts_feature WHERE account_id = %s", (student_id,))

        result = cur.fetchall()

        if result:
            print("UPDATE", student_id)
            cur.execute("UPDATE accounts_feature SET vector=%s WHERE account_id=%s", (string_features_vector, student_id))
        else:
            print("INSERT", student_id)
            cur.execute("INSERT INTO accounts_feature (account_id, vector) VALUES (%s, %s)", (student_id, string_features_vector))

        cur.connection.commit()
        cur.close()
    except Exception as e:
        print('Error in face_recognization: ', str(e))


















