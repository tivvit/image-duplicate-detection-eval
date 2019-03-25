FROM python

WORKDIR /app

RUN pip install \
    imagehash \
    sklearn

COPY *.py /app/

CMD python3 eval.py