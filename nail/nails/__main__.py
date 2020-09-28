from flask import Flask, request, jsonify
import keras
import cv2
import os
import tensorflow as tf
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

side = 299
med_model = keras.models.Sequential()
graph = []
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)
tf.logging.set_verbosity(tf.logging.ERROR)


def create_app():
    app = Flask(__name__)

    def run_on_start(*args, **argv):
        global graph, med_model
        print(f'[INIT][NAIL] ANN initialization started')
        with open('[NAIL]model_conv.yaml', 'r') as yaml_file:
            loaded_model_yaml = yaml_file.read()
            med_model = keras.models.model_from_yaml(loaded_model_yaml)
            med_model.load_weights('[NAIL]model_conv.h5')
            graph = tf.get_default_graph()
        print('[INIT][NAIL] ANN initialized')
        print(f'AURA system standby...')

    run_on_start()
    return app


app = create_app()


@app.route('/ping')
def pingpong():
    return 'pong'


@app.route('/check', methods=['POST'])
def check_image():
    r = request
    imarr = np.fromstring(r.data, np.uint8)
    image = cv2.imdecode(imarr, cv2.IMREAD_COLOR)
    # cv2.imshow('RECEIVED', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    resized = cv2.resize(image, (side, side))
    resized = (resized[..., ::-1].astype(np.float32)) / 255.0
    reshaped = resized.reshape(1, side, side, 3)
    with graph.as_default():
        out = med_model.predict(reshaped)
    respond = [str(out[0][0]), str(out[0][1]), str(out[0][2])]

    return jsonify(respond)


if __name__ == '__main__':
    app.run(debug=False, port=8000, use_reloader=False)
