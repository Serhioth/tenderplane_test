FROM python:3.12

WORKDIR /parser

COPY requirements.txt ./

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "-m", "main"]