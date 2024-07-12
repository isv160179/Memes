FROM python:3.9.19


WORKDIR /memes
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt --no-cache-dir
COPY .. .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
