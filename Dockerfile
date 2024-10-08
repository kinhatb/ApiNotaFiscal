FROM python:3.10-slim

RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev libleptonica-dev

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]