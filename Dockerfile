FROM python:3.12

WORKDIR /app

# System deps: gettext-base provides msguniq/msgfmt
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     build-essential \
     gettext \
     gettext-base \
     python3-cffi \
  && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
  && pip install -r requirements.txt

# App code
COPY . /app

ENV PYTHONUNBUFFERED=1

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
