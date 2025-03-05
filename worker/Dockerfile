FROM python:3.10

WORKDIR /worker

COPY requirements.txt ./

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .
