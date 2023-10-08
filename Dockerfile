FROM python:3.8-slim

WORKDIR /surf_app

COPY requirements.txt ./
COPY app ./
COPY libs ./
COPY server_params ./
COPY config ./
COPY main.py ./

RUN pip install /requirements.txt

CMD ["python", "main.py"]
