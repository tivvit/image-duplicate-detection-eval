from __future__ import print_function

import io
import json
import sys
import time
from glob import glob
import numpy as np

import tensorflow as tf
from PIL import Image
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


def get_image_bytes(file_path=None, pil_image=None):
    if file_path:
        img = Image.open(file_path)
    else:
        img = pil_image
    img_bytes = io.BytesIO()
    img.convert("RGBA").save(img_bytes, format='PNG')
    return img_bytes.getvalue()


def extract_features(file_path=None, pil_image=None):
    try:
        data = get_image_bytes(file_path=file_path, pil_image=pil_image)
        return get_result("resnet", data)
    except Exception:
        print("{} failed".format(file_path))


def get_result(model, data, outputs="scores", signature_name="predict_images"):
    """
      Args:
        model: name of model to be used for processing
        data: data to be processed
      Returns:
        The classification vector.

      Raises:
        IOError: An error occurred processing test data set.
    """
    host = "tf-serving"
    port = 2233
    timeout = 1
    channel = implementations.insecure_channel(host, int(port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    request = predict_pb2.PredictRequest()
    request.model_spec.name = model
    request.model_spec.signature_name = signature_name
    request.inputs['inputs'].CopyFrom(
        tf.contrib.util.make_tensor_proto(data))
    result_future = stub.Predict.future(request, timeout)  # 5 seconds
    iter_outputs = [outputs]
    tf_response = result_future.result()
    result = []
    for o in iter_outputs:
        response = tf_response.outputs[o]
        result.append(tf.contrib.util.make_ndarray(response))
    return np.ndarray.tolist(result[0][0][0][0])


if __name__ == '__main__':
    print("Wait for TF serving start")
    time.sleep(2)
    with open("/out/features.json", "w") as f:
        g = glob("/data/*")
        l = len(g)
        c = 0
        for i in g:
            features = extract_features(file_path=i)
            c += 1
            print("{}/{}".format(c, l))
            if features:
                f.write(json.dumps([i, features]) + '\n')
