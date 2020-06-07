FROM tiangolo/uvicorn-gunicorn-starlette:python3.7-alpine3.8

COPY requirements /app/requirements

RUN pip install -r /app/requirements/prod.txt

COPY . /app
