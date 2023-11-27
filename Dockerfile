FROM python:3.6-buster
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY static .
COPY templates .
COPY *.csv .
COPY 
CMD ["python", "app.py"]