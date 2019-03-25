FROM python

WORKDIR /app

RUN pip install \
    Pillow \
    scikit-image

COPY *.py /app

CMD python3 alternate.py