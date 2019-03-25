FROM python:2.7.14
#FROM python

RUN pip install --upgrade pip
RUN pip install grpcio \
    tensorflow-serving-api \
    pillow
#  tensorflow

#RUN mkdir /tfs/
#COPY sample.conf /www/email/szn-tensorflow-serving/conf/models.autoconf
#COPY sample /tfs/sample
#COPY probes.py /probes.py
WORKDIR /app
COPY extract_features.py .


CMD python extract_features.py