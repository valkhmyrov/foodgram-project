FROM python:3.8.5
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get install -y netcat
RUN apt-get update
COPY . .
CMD gunicorn foodgram_project.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --access-logfile '-' --error-logfile '-'