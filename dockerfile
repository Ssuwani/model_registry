FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

RUN apt update -y && \
apt upgrade -y && \
apt install build-essential -y && \
apt install libhdf5-dev -y && \
pip install poetry==1.7.0 && \
poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./

RUN poetry install --only main --no-interaction

COPY ./ /app

EXPOSE 5000

ENTRYPOINT uvicorn app:app --host 0.0.0.0 --port 5001