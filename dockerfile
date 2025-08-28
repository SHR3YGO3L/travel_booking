# Use official Python image as base
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /travel_booking

# Install system dependencies (for mysqlclient if you use MySQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt /travel_booking/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /travel_booking/

# Collect static files (if you use static file serving)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
