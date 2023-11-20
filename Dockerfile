FROM python:3.10

WORKDIR app

COPY server_requirements.txt .
RUN pip install -r server_requirements.txt

COPY src/server_config.py .
COPY src/server.py .
COPY .env .

CMD ["uvicorn", "server:guruzee", "--host=0.0.0.0", "--port=8000"]
