FROM python:3.11

WORKDIR /backend
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["uvicorn", "backend.main:app", "--reload"] 
