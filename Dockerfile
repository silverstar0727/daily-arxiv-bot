FROM python:3.9

WORKDIR /workspace

COPY requirements.txt .

RUN pip install -r requirements.txt
EXPOSE 3000

COPY . .

ENTRYPOINT ["uvicorn", "main:api", "--reload", "--host", "0.0.0.0", "--port", "3000"]