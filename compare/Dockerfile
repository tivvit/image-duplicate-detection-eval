FROM python

WORKDIR /app

RUN pip install \
    Pillow \
    imagehash

COPY *.py /app

CMD python3 compare.py