# Use official Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies (including OpenSSL for SSL support)
RUN apt-get update && apt-get install -y \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first (for efficient caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project
COPY . .

# Copy the SSL certificate and key files into the container
COPY certs/certificate.crt /etc/ssl/certs/
COPY certs/private.key /etc/ssl/private/

# Expose port 443 for HTTPS
EXPOSE 8000

# Run migrations and start the Django server with SSL
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver"]
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runsslserver --certificate /etc/ssl/certs/certificate.crt --key /etc/ssl/private/private.key 0.0.0.0:443"]
