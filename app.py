from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for
import tensorflow_hub as hub
from tensorflow.keras.utils import load_img, img_to_array
import tensorflow as tf
import os
import numpy as np

from keras.models import load_model
import cv2
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
modelo = tf.keras.models.load_model(
    ('clasificador_marcas.h5'),
    custom_objects={'KerasLayer': hub.KerasLayer}
)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


@app.route('/')
def hello_world():
    return 'Hola mundo'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            try:
                print("iniciando creación de folder")
                os.stat(UPLOAD_FOLDER)
            except:
                os.mkdir(UPLOAD_FOLDER)
            print("iniciando guardado de archivo")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print("iniciando prediccion")
            prediccion = categorizar(UPLOAD_FOLDER+'/'+filename)
            os.remove(UPLOAD_FOLDER+'/'+filename)
            return prediccion_(prediccion)


def categorizar(path):
    img = load_img(path)
    img = np.array(img).astype(float)/255
    img = cv2.resize(img, (224, 224))
    prediccion = modelo.predict(img.reshape(-1, 224, 224, 3))
    print("prediccion", prediccion[0])
    return np.argmax(prediccion[0], axis=-1)


def prediccion_(prediccion):
    if prediccion == 0:
        return "boing"
    if prediccion == 1:
        return "bonafont"
    if prediccion == 2:
        return "ciel"
    if prediccion == 3:
        return "coca"
    if prediccion == 4:
        return "colgate"
    if prediccion == 5:
        return "corona"
    if prediccion == 6:
        return "costena"
    if prediccion == 7:
        return "danone"
    if prediccion == 8:
        return "electrolit"
    if prediccion == 9:
        return "fanta"
    if prediccion == 10:
        return "fresca"
    if prediccion == 11:
        return "garnier"
    if prediccion == 12:
        return "greatvalue"
    if prediccion == 13:
        return "herdez"
    if prediccion == 14:
        return "jumex"
    if prediccion == 15:
        return "lala"
    if prediccion == 16:
        return "nestlee"
    if prediccion == 17:
        return "nivea"
    if prediccion == 18:
        return "pepsi"
    if prediccion == 19:
        return "saba"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
