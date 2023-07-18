# Use an official Python runtime as the base image
FROM    python:3.10-slim

# Set the working directory in the container
WORKDIR /app

RUN  set -ex; \
        # For psql binary / postgres
        mkdir -p /usr/share/man/man1 /usr/share/man/man7; \
        apt-get update && \
        apt-get install -y --no-install-recommends \
        xmlsec1 \
        libxmlsec1-dev \
        libjpeg-dev \
        libyajl2 \
        libpq-dev \
        libpq5 \
        gcc \
        postgresql-client \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY ./app/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY ./app /app/

# Expose the port that the Django app will run on
EXPOSE 8000

# Start the Django development server
CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]