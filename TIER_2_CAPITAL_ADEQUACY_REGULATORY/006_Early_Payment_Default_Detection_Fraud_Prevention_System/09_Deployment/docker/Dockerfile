FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Logistic_Regression_model.pkl .
COPY scaler.pkl .
COPY features.json .
COPY app.py .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "30", "app:app"]
