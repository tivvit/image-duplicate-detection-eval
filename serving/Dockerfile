FROM ubuntu:xenial

RUN echo "deb [arch=amd64] http://storage.googleapis.com/tensorflow-serving-apt stable tensorflow-model-server tensorflow-model-server-universal" | tee /etc/apt/sources.list.d/tensorflow-serving.list

RUN apt-get update && apt-get install -y curl gnupg2

RUN curl https://storage.googleapis.com/tensorflow-serving-apt/tensorflow-serving.release.pub.gpg | apt-key add -

RUN apt-get update && \
    apt-get install -y --allow-unauthenticated \
    tensorflow-model-server-universal \
    && rm -rf /var/lib/apt/lists/*

COPY model.conf /

CMD ["tensorflow_model_server", "--port=2233", "--model_config_file=/model.conf"]
