# Use official Python image as the base
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first (for efficient caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project
COPY . .

# Expose port 8000 (Django default)
EXPOSE 8000

# Run migrations and start the Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
